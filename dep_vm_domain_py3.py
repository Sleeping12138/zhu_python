# -*- coding: utf-8 -*-
# !/bin/python2
import argparse
import getpass
import io
import logging
import logging.handlers
import multiprocessing
import os
import random
import re
import shutil
import subprocess
import time
import string
import uuid
import traceback
import datetime
import pytz
import xml.dom.minidom
import xml.etree.ElementTree as ET
import zipfile
import stat
import zipfile
import random
import string
from multiprocessing.pool import ThreadPool

import requests

log = logging.getLogger()

base_name_map = {
    "centos7_x86_64_everything_base": "centos7.qcow2",
    "kylin_desktop_v10_base": "kylin.qcow2",
    "ubuntu1704_amd64_desktop_base": "ubuntu1704.qcow2",
    "win10_1903_x64_2016_base": "win10_1903_x64_2016.qcow2",
    "hygon_amd64_desktop_v20_base": "hygon_amd64_desktop_v20.qcow2",
    "win7_sp1_x64_2013_base": "win7.qcow2",
    "win7_sp1_x86_2003_base": "win7.qcow2",
    "win7_sp1_x86_2007_base": "win7.qcow2",
    "win7_sp1_x86_2010_base": "win7.qcow2",
    "win7_sp1_x86_2013_base": "win7.qcow2",
    "macos_13_x86_64_base": "macos_13_x86_64.qcow2",
    "redhat7_server_x86_64_base": "redhat7_server_x86_64.qcow2",
}
sandbox_type_base_map = {
    "centos7": "centos7_x86_64_everything_base",
    "kylin_desktop_v10": "kylin_desktop_v10_base",
    "ubuntu1704": "ubuntu1704_amd64_desktop_base",
    "win10_x64_office2016": "win10_1903_x64_2016_base",
    "win7_x64_office2013": "win7_sp1_x64_2013_base",
    "win7_office2003": "win7_sp1_x86_2003_base",
    "win7_office2007": "win7_sp1_x86_2007_base",
    "win7_office2010": "win7_sp1_x86_2010_base",
    "win7_office2013": "win7_sp1_x86_2013_base",
    "hygon_desktop_v20": "hygon_amd64_desktop_v20_base",
    "macos_13_x86_64": "macos_13_x86_64_base",
    "redhat7": "redhat7_server_x86_64_base",
}
conf_child_vm_labe_100 = {
    "ubuntu1704": {"label": "ubuntu1704_amd64-", "base_ip_head": "100.64.1.", "base_ip": 10, "count": 20,
                   "mitm_base_port": 50000, "platform": "linux", "tag": ""},
    "centos7": {"label": "centos7_x86_64-", "base_ip_head": "100.64.2.", "base_ip": 10, "count": 20,
                "mitm_base_port": 50500, "platform": "linux", "tag": ""},
    "win7_office2003": {"label": "win7_sp1_x86_2003-", "base_ip_head": "100.64.3.", "base_ip": 10, "count": 10,
                        "mitm_base_port": 51000, "platform": "windows", "tag": ""},
    "win7_office2007": {"label": "win7_sp1_x86_2007-", "base_ip_head": "100.64.4.", "base_ip": 10, "count": 10,
                        "mitm_base_port": 51500, "platform": "windows", "tag": ""},
    "win7_office2010": {"label": "win7_sp1_x86_2010-", "base_ip_head": "100.64.5.", "base_ip": 10, "count": 10,
                        "mitm_base_port": 52000, "platform": "windows", "tag": ""},
    "win7_office2013": {"label": "win7_sp1_x86_2013-", "base_ip_head": "100.64.6.", "base_ip": 10, "count": 20,
                        "mitm_base_port": 52500, "platform": "windows", "tag": ""},
    "win7_x64_office2013": {"label": "win7_sp1_x64_2013-", "base_ip_head": "100.64.7.", "base_ip": 10, "count": 20,
                            "mitm_base_port": 53000, "platform": "windows", "tag": ""},
    "win10_x64_office2016": {"label": "win10_1903_x64_2016-", "base_ip_head": "100.64.8.", "base_ip": 10,
                             "count": 20, "mitm_base_port": 53500, "platform": "windows", "tag": ""},
    "kylin_desktop_v10": {"label": "kylin_desktop_v10-", "base_ip_head": "100.64.9.", "base_ip": 10, "count": 10,
                          "mitm_base_port": 54000, "platform": "linux", "tag": ""},
    "hygon_desktop_v20": {"label": "hygon_desktop_v20-", "base_ip_head": "100.64.10.", "base_ip": 10, "count": 10,
                          "mitm_base_port": 54500, "platform": "linux", "tag": ""},
    "macos_13_x86_64": {"label": "macos_13_x86_64-", "base_ip_head": "100.64.11.", "base_ip": 10, "count": 20,
                        "mitm_base_port": 54600, "platform": "darwin", "tag": ""},
    "redhat7": {"label": "redhat7_x86_64-", "base_ip_head": "100.64.12.", "base_ip": 10, "count": 10,
                "mitm_base_port": 54700, "platform": "linux", "tag": ""},

}

conf_child_vm_label_192 = {
    "ubuntu1704": {"label": "ubuntu1704_amd64-", "base_ip_head": "192.168.1.", "base_ip": 10, "count": 20,
                   "mitm_base_port": 50000, "platform": "linux", "tag": ""},
    "centos7": {"label": "centos7_x86_64-", "base_ip_head": "192.168.2.", "base_ip": 10, "count": 20,
                "mitm_base_port": 50500, "platform": "linux", "tag": ""},
    "win7_office2003": {"label": "win7_sp1_x86_2003-", "base_ip_head": "192.168.3.", "base_ip": 10, "count": 10,
                        "mitm_base_port": 51000, "platform": "windows", "tag": ""},
    "win7_office2007": {"label": "win7_sp1_x86_2007-", "base_ip_head": "192.168.4.", "base_ip": 10, "count": 10,
                        "mitm_base_port": 51500, "platform": "windows", "tag": ""},
    "win7_office2010": {"label": "win7_sp1_x86_2010-", "base_ip_head": "192.168.5.", "base_ip": 10, "count": 10,
                        "mitm_base_port": 52000, "platform": "windows", "tag": ""},
    "win7_office2013": {"label": "win7_sp1_x86_2013-", "base_ip_head": "192.168.6.", "base_ip": 10, "count": 20,
                        "mitm_base_port": 52500, "platform": "windows", "tag": ""},
    "win7_x64_office2013": {"label": "win7_sp1_x64_2013-", "base_ip_head": "192.168.7.", "base_ip": 10,
                            "count": 20, "mitm_base_port": 53000, "platform": "windows", "tag": ""},
    "win10_x64_office2016": {"label": "win10_1903_x64_2016-", "base_ip_head": "192.168.8.", "base_ip": 10,
                             "count": 20, "mitm_base_port": 53500, "platform": "windows", "tag": ""},
    "kylin_desktop_v10": {"label": "kylin_desktop_v10-", "base_ip_head": "192.168.9.", "base_ip": 10, "count": 10,
                          "mitm_base_port": 54000, "platform": "linux", "tag": ""},
    "hygon_desktop_v20": {"label": "hygon_desktop_v20-", "base_ip_head": "192.168.10.", "base_ip": 10, "count": 10,
                          "mitm_base_port": 54500, "platform": "linux", "tag": ""},
    "macos_13_x86_64": {"label": "macos_13_x86_64-", "base_ip_head": "192.168.11.", "base_ip": 10, "count": 20,
                        "mitm_base_port": 54600, "platform": "darwin", "tag": ""},
    "redhat7": {"label": "redhat7_x86_64-", "base_ip_head": "192.168.12.", "base_ip": 10, "count": 10,
                "mitm_base_port": 54700, "platform": "linux", "tag": ""},

}


# virsh list --all |grep shut|awk '{print $2}' |grep "-"|xargs -I {} virsh undefine {}  --snapshots-metadata
# rm -rf centos7_x86_64-* kylin_desktop_v10-* ubuntu1704_amd64-* win10_1903_x64_2016-* win7_sp1_x64_2013-* win7_sp1_x86_2003-*

def add_try_except(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            log.error(traceback.format_exc())

    return wrapper


def generate_mac_address():
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    mac[0] = (mac[0] & 0xfc) | 0x02
    mac_address = ':'.join(['%02x' % x for x in mac])
    return mac_address


def init_logger(level=logging.DEBUG):
    global log
    try:
        formatter = logging.Formatter(
            "%(asctime)s [%(name)s] [%(filename)s %(lineno)d] %(levelname)s: %(message)s"
        )
        log_file_path_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log_dep_vm_domain.log")
        l = logging.handlers.RotatingFileHandler(log_file_path_name, maxBytes=50 * 1024 * 1024, backupCount=2)
        l.setFormatter(formatter)
        l.setLevel(level)
        log = logging.getLogger()
        # log.addHandler(l)
        log.setLevel(level)
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        log.addHandler(sh)
        log.addHandler(l)
        logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    except Exception as e:
        print((traceback.format_exc()))


# def get_mac_ip():
#     for key, value in conf_child_vm_label.iteritems():
#         label = value['label']
#         base_ip_head = value['base_ip_head']
#         base_ip = value['base_ip']
#         count = value['count']
#         # print(label, base_ip_head, base_ip, count)
#         for i in range(1, count + 1):
#             ip_address = base_ip_head + str(base_ip + i)
#             domain_id = label + str(i)
#             # print(domain_id,data_dict[domain_id],ip_address)
#             tag = "      <host mac='{mac}' ip='{ip}'/>".format(mac=data_dict[domain_id], ip=ip_address)
#             log.info(tag)

def generate_random_string(length):
    # First character must be a letter
    first_char = random.choice(string.ascii_uppercase)
    # Remaining characters are alphanumeric
    rest_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length - 1))
    return first_char + rest_chars

@add_try_except
def generate_network_xml(origin_xml_path, conf_label, save_xml_path):
    if os.path.exists(save_xml_path):
        print((save_xml_path + " already exists"))
    data_dict_id_mac = {}
    tree = ET.parse(origin_xml_path)
    root = tree.getroot()
    dhcp_element = root.find(".//dhcp")
    if not os.path.exists("./gen"):
        os.mkdir("./gen")
    for key, value in conf_label.items():
        label = value['label']
        base_ip_head = value['base_ip_head']
        base_ip = value['base_ip']
        count = value['count']
        # win10 count=80
        if label == "win10_1903_x64_2016-" and count < 80:
            count = 80
        # print(label, base_ip_head, base_ip, count)
        g_path = "./gen/id_mac" + ".dat.gen_" + label
        if os.path.exists(g_path):
            print(("genfile exists " + g_path + " load to file"))
            with open(g_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    splits = line.strip().split(" ")
                    mac_id = splits[1]
                    ip_address = splits[2]
                    new_host_element = ET.Element("host", mac=mac_id, ip=ip_address)
                    dhcp_element.append(new_host_element)
            continue
        output_file = open(g_path, "w")
        for i in range(1, count + 1):
            ip_address = base_ip_head + str(base_ip + i)
            domain_id = label + str(i)
            data_dict_id_mac[domain_id] = generate_mac_address()
            new_host_element = ET.Element("host", mac=data_dict_id_mac[domain_id], ip=ip_address)
            dhcp_element.append(new_host_element)
            output_file.write(domain_id + " " + data_dict_id_mac[domain_id] + " " + ip_address + "\n")
        output_file.close()
    xml_data = ET.tostring(root, encoding="utf-8")
    # print(type(xml_data))
    dom = xml.dom.minidom.parseString(xml_data.decode().replace("\n", "").replace("\r\n", "").encode('utf-8'))
    pretty_xml_str = dom.toprettyxml(indent="  ")
    output_file = open(save_xml_path, "w")
    output_file.write(pretty_xml_str)
    output_file.close()


def undefine_all_domain(conf_child_vm_label):
    for key, value in conf_child_vm_label.items():
        label = value['label']
        base_ip_head = value['base_ip_head']
        base_ip = value['base_ip']
        count = value['count']
        # print(label, base_ip_head, base_ip, count)
        for i in range(1, count + 1):
            domain_id = label + str(i)
            info = os.popen("virsh undefine %s" % domain_id).read()
            log.info("define undefine - %s" % (info))


@add_try_except
def deploy_vm(sandbox_type, data_dict, qemu_kvm_dir, value):
    log.info(" current {} started ".format(sandbox_type))
    label = value['label']
    base_ip_head = value['base_ip_head']
    base_ip = value['base_ip']
    count = value['count']
    if label == "win10_1903_x64_2016-" and get_cpu_cores() > 90 and is_hygon_cpu():
        count = 80

    # print(label, base_ip_head, base_ip, count)
    start_time = time.time()
    cpu_count = multiprocessing.cpu_count()
    parallel_threads = cpu_count // 3
    thread_pool = ThreadPool(processes=parallel_threads)
    async_results = []
    for i in range(1, count + 1):
        ip_address = base_ip_head + str(base_ip + i)
        domain_id = label + str(i)
        mac = data_dict[domain_id]
        base_path_name = sandbox_type_base_map[sandbox_type]
        base_image_path = os.path.join(qemu_kvm_dir, base_path_name, base_name_map[base_path_name])
        log.info(domain_id + " current {} {} {} ".format(base_image_path, domain_id, ip_address))
        async_results += [thread_pool.apply_async(define_domain_create_snapshot,
                                                  args=(base_image_path, domain_id, ip_address, mac, qemu_kvm_dir))]
    for i in range(1, count + 1):
        domain_id = label + str(i)
        is_ok = async_results[i - 1].get()
        if is_ok:
            log.info("[OK] create snapshot - %s" % (domain_id))
        else:
            log.error("[FAIL] create snapshot - %s" % (domain_id))
    thread_pool.close()
    thread_pool.join()
    end_time = time.time()
    log.info(" current {} completed use time {}".format(sandbox_type, end_time - start_time))


def run_cmd(cmd):
    returncode = -1
    out = ""
    err = ""
    try:
        if isinstance(cmd, str):
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log.debug(cmd)
        elif isinstance(cmd, list):
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log.debug(" ".join(cmd))
        out, err = p.communicate()
        returncode = p.returncode
        if returncode != 0:
            pass
            log.warning(
                "{} -> returncode: {}, out: {}, err: {}".format(cmd, p.returncode, str(out).replace("\n", ""),
                                                                      str(err).replace("\n", "")))
        else:
            pass
            log.debug(
                "{} -> returncode: {}, out: {}, err: {}".format(cmd, p.returncode, str(out).replace("\n", ""),
                                                                      str(err).replace("\n", "")))
    except Exception as e:
        log.error("run {}, exception: {}".format(cmd, traceback.format_exc()))
    return returncode, out.decode(), err.decode()


def zip_dir(dir):
    zip_data = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_data, "w", zipfile.ZIP_STORED)
    root_dir = os.path.abspath(dir)
    root_len = len(os.path.dirname(root_dir))
    for root, dirs, files in os.walk(root_dir):
        archive_root = os.path.abspath(root)[root_len:]
        for name in files:
            path = os.path.join(root, name)
            archive_name = os.path.join(archive_root, name)
            zip_file.write(path, archive_name)
    zip_file.close()
    data = zip_data.getvalue()
    return data


def get_from_vm(url_front, method, *args, **kwargs):
    """Simple wrapper around requests.get()."""
    url = "{}/%s" % (url_front, method)
    session = requests.Session()
    session.trust_env = False
    session.proxies = None
    r = session.get(url, *args, **kwargs)
    return r


def post_to_vm(url_front, method, *args, **kwargs):
    """Simple wrapper around requests.post()."""
    url = "%s%s" % (url_front, method)
    session = requests.Session()
    session.trust_env = False
    session.proxies = None
    r = session.post(url, *args, **kwargs)
    # r.status_code
    # r.content -> r.json()
    return r


def store_to_vm(url_front, host_file_path_name, file_in_vm_path):
    data = {"filepath": "{}".format(file_in_vm_path)}
    files = {
        "file": ("some_name", open(host_file_path_name, "rb")),
    }
    rep = post_to_vm(url_front, "/store", files=files, data=data, timeout=30)
    return "/store", rep.content

def set_clock(url_front):
    try:
        tz_settting = "Asia/Shanghai"
        tz = pytz.timezone(tz_settting)
        dt = datetime.datetime.now(tz=tz)
        str_clock = dt.strftime("%Y-%m-%d %H:%M:%S.%f %z")
        json_data = {"clock": str_clock}
        r = post_to_vm(url_front, "/synclock", data=json_data, timeout=40)
        if (r.status_code != 200) and r.content:
            log.warning("set clock error: {}".format(r.json()))
            return False
        log.debug("set clock success: {}".format(r.json()))
    except Exception as e:
        log.error("set clock error: {}".format(e))
    return True

def minimize_show_desktop(url_front):
    is_ok = False
    try:
        ok_count = 0
        cmd_list = [
            "c:\\python27\\python.exe -c \"import win32gui, win32con; win32gui.EnumWindows(lambda hwnd, _: win32gui.ShowWindow(hwnd, win32con.SW_FORCEMINIMIZE) if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) else None, None)\"",
            "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -command \"(New-Object -ComObject shell.application).MinimizeAll()\"",
        ]
        for cmd in cmd_list:
            data = {
                "command": cmd,
                "cwd": "C:\\",
            }
            r = post_to_vm(url_front, "/execute", data=data, timeout=30)
            if r.status_code != 200:
                if r.content:
                    log.debug(r.json())
            else:
                ok_count += 1
                log.debug("minimize to show desktop success: {}".format(r.json()))
        is_ok = ok_count == len(cmd_list)
    except Exception as e:
        log.error("minimize to show desktop error: {}".format(e))
    return is_ok


def init_env_win10(url_front, domain_id):
    is_rename_ok = False
    try:
        vm_dirpath = "C:\\install"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pre_init_env_vm_file_path = vm_dirpath + "\\pre_init_env.py"
        # 4. execute python pre_init_env.py -mode=rename
        data = {
            "command": "C:\\Python27\\pythonw.exe \"{}\" -mode=rename".format(pre_init_env_vm_file_path),
            "cwd": vm_dirpath,
        }
        r = post_to_vm(url_front, "/execute", data=data, timeout=40)
        if (r.status_code != 200) and r.content:
            log.debug(r.json())

        data = {"filepath": vm_dirpath + "\\" + "log_pre_init_env.log"}
        r = post_to_vm(url_front, "/retrieve", data=data, timeout=20)
        if b"[OK] rename user name" in r.content:
            is_rename_ok = True
            log.debug("ok rename user name for {}".format(domain_id))
        else:
            log.warning("fail rename user name for {}".format(domain_id))
        log_pre_init_in_host_file_path = os.path.join(current_dir, "vm", "windows",
                                                      "{}_log_pre_init_env_rename.log".format(domain_id))
        with open(log_pre_init_in_host_file_path, 'wb') as f:
            f.write(r.content)
    except Exception as e:
        log.error("init env {} exception: {}".format(domain_id, traceback.format_exc()))
    return is_rename_ok



def clean_pre_init_scripts_win10(url_front, domain_id, is_rename_ok):
    try:
        vm_dirpath = "c:\\install"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        host_py_file_path = os.path.join(current_dir, "vm", "windows", "clean_%s.py" % (domain_id))
        vm_py_file_path = "C:\\windows\\clean.py"
        content = "import os,shutil\ntry:\n  shutil.rmtree(r\"%s\")\nexcept:\n  pass\n" % (vm_dirpath)
        if is_rename_ok:
            tmp_user_path = "C:\\Users\\tmp"
            tmp_user_rename_path = "C:\\Users\\Guest"
            content += "try:\n  os.rename(r\"%s\", r\"%s\")\n  shutil.rmtree(r\"%s\")\n  os.system(r'C:\\Windows\\system32\\cmd.exe /c rmdir /s /q \"%s\"')\nexcept:\n  pass\n" % (
                tmp_user_path, tmp_user_rename_path, tmp_user_rename_path, tmp_user_rename_path)
        content += "try:\n  os.system(r'C:\\Windows\\system32\\cmd.exe /c del \"%s\"')\nexcept:\n  pass" % (
            vm_py_file_path)
        with open(host_py_file_path, 'w') as f:
            f.write(content)
        store_to_vm(url_front, host_py_file_path, vm_py_file_path)

        data = {
            "command": "C:\\Python27\\pythonw.exe \"%s\"" % (vm_py_file_path),
            "cwd": "c:\\",
        }
        r = post_to_vm(url_front, "/execute", data=data)  # , timeout=20
        if (r.status_code != 200) and r.content:
            log.debug(r.json())
    except Exception as e:
        log.error("clean pre init env {} exception: {}".format(domain_id, traceback.format_exc()))
    finally:
        try:
            if os.path.exists(host_py_file_path):
                os.remove(host_py_file_path)
        except Exception as e1:
            log.error(traceback.format_exc())

@add_try_except
def shutdown_vm(domain_id, prefix):
    info = os.popen("virsh shutdown %s" % domain_id).read()
    log.info(prefix + " shutdown %s - %s  20 " % (domain_id, info.replace("\n", " ")))
    log.debug("waiting {} shutdown max 50s".format(domain_id))
    tick_count = 0
    is_ok = False
    vm_status = ""
    while tick_count < 50:
        time.sleep(6)
        tick_count += 6
        ret, out, err = run_cmd("virsh domstate " + domain_id)
        vm_status = out.strip()
        if "shut off" == vm_status:
            is_ok = True
            log.debug("[OK] {} shutdown ok".format(domain_id))
            break
    if not is_ok:
        log.warning("[FAIL] shutdown {}, status: {}, force stop it.".format(domain_id, vm_status))
        run_cmd("virsh destroy %s" % domain_id)

def restart_vm(domain_id, prefix):
    log.info("win restart " + domain_id)
    shutdown_vm(domain_id, prefix)
    info = os.popen("virsh start %s" % domain_id).read()
    log.info(prefix + "start %s - wait 5 " % (info.replace("\n", " ")))

def is_qcow2(file_path_name):
    is_match = False
    try:
        with open(file_path_name, 'rb') as f:
            data = f.read(4)
        is_match = True if data == b"QFI\xfb" else False
    except Exception as e:
        log.error("is qcow2 exception:{}".format(e))
        return False
    return is_match

def rebuild_clone_xml(base_image_path, new_vm_xml_file_path, new_vm_macaddr, new_vm_image_path, new_vm_domain_id):
    # read in
    new_vm_instance_dir = os.path.dirname(new_vm_xml_file_path)
    if not os.path.exists(new_vm_instance_dir):
        os.mkdir(new_vm_instance_dir)
    base_vm_dir = os.path.dirname(base_image_path)
    base_domain_xml = ""
    for name in os.listdir(base_vm_dir):
        if name.endswith(".xml"):
            base_domain_xml = os.path.join(base_vm_dir, name)
    if not os.path.exists(base_domain_xml):
        log.info("没有母盘配置文件 " + base_domain_xml)
        return False
    fd = open(base_domain_xml, "r")
    xml_buffer = fd.read()
    fd.close()

    names = re.findall(r"<name>([\w,-]{0,100})</name>", xml_buffer)
    if len(names) < 1:
        log.info("母盘没有注册 " + base_domain_xml + " " + new_vm_domain_id + str(xml_buffer))
        return False

    base_image_xml = os.path.join(os.path.dirname(base_vm_dir), names[0] + ".xml")
    log.info("模板 %s %s" % (new_vm_domain_id, base_image_xml))
    fd = open(base_image_xml, "r")
    xml_buffer = fd.read()
    fd.close()

    # delete => MAC

    xml_buffer_new = re.sub('(<mac address=)(.*?)(/>)', r'\1"' + new_vm_macaddr + r'"\3', xml_buffer)
    if new_vm_domain_id.startswith("mac"):
        # 1. <loader readonly="yes" type="rom">/data/qemu_kvm/macos_13_x86_64_base/OVMF_CODE.fd</loader>
        #  <loader readonly="yes" type="pflash">/data/qemu_kvm/macos_13_x86_64_base/OVMF_CODE.fd</loader>
        base_file_path = os.path.join(base_vm_dir, "OVMF_CODE.fd")
        new_file_path = os.path.join(new_vm_instance_dir, "OVMF_CODE.fd")
        fd_new_file_path = os.path.join(new_vm_instance_dir, "OVMF_CODE.fd")
        copy_cmd = "cp -f \"%s\" \"%s\"" % (base_file_path, new_file_path)
        code, inf, error = run_cmd(copy_cmd)
        if code:
            log.error("{} -> ret: {}, info: {}, err: {}".format(copy_cmd, code, inf, error))
            return False
        log.debug("{} -> ret: {}".format(copy_cmd, code))
        xml_buffer_new = re.sub("(<loader readonly='yes' type='rom'>)(.*?)(</loader>)",
                                r'\1' + new_file_path + r'\3',
                                xml_buffer_new)
        # 2. <nvram>/data/qemu_kvm/macos_13_x86_64_base/OVMF_VARS.fd</nvram>
        base_file_path = os.path.join(base_vm_dir, "OVMF_VARS.qcow2")
        new_file_path = os.path.join(new_vm_instance_dir, "OVMF_VARS.qcow2")
        qcow2_new_file_path = os.path.join(new_vm_instance_dir, "OVMF_VARS.qcow2")
        copy_cmd = "cp -f \"%s\" \"%s\"" % (base_file_path, new_file_path)
        code, inf, error = run_cmd(copy_cmd)
        if code:
            log.error("{} -> ret: {}, info: {}, err: {}".format(copy_cmd, code, inf, error))
            return False
        log.debug("{} -> ret: {}".format(copy_cmd, code))
        xml_buffer_new = re.sub('(<nvram>)(.*?)(</nvram>)',
                                r'\1' + new_file_path + r'\3',
                                xml_buffer_new)
        # 3. <source file="/data/qemu_kvm/macos_13_x86_64_base/OpenCore.qcow2"/>
        base_file_path = os.path.join(base_vm_dir, "OpenCore.qcow2")
        new_file_path = os.path.join(new_vm_instance_dir, "OpenCore.qcow2")
        copy_cmd = "qemu-img create -f qcow2 -b \"%s\" -F qcow2 \"%s\"  " % (base_file_path, new_file_path)
        code, inf, error = run_cmd(copy_cmd)
        if code:
            log.error("{} -> ret: {}, info: {}, err: {}".format(copy_cmd, code, inf, error))
            return False
        log.debug("{} -> ret: {}".format(copy_cmd, code))
        xml_buffer_new = re.sub("(<source file=)('.*OpenCore\.qcow2')(.*/>)", r"\1'" + new_file_path + r"'\3",
                                xml_buffer_new)
        # 定义正则表达式和替换字符串
        nvram_format="qcow2"
        pattern = r'(<nvram\s*.*?)>(.*?)(</nvram>)'
        replacement = f"<nvram template='{fd_new_file_path}' format='{nvram_format}'>{qcow2_new_file_path}</nvram>"
        # 使用 re.sub 进行替换
        xml_buffer_new = re.sub(pattern, replacement, xml_buffer_new )
        # print(xml_buffer_new)
        # 4. <source file="/data/qemu_kvm/macos_13_x86_64_base/macos_13_x86_64.qcow2"/>
        xml_buffer_new = re.sub("(<source file=)('%s')(/>)" % (base_image_path), r"\1'" + new_vm_image_path + r"'\3",
                                xml_buffer_new)
    else:
        xml_buffer_new = re.sub("(<source file=)(.*?)(/>)", r"\1'" + new_vm_image_path + r"'\3", xml_buffer_new)
    xml_buffer_new = re.sub('\s*<uuid>.*?</uuid>', "", xml_buffer_new)

    def replace_topology(match):
        if is_hygon_cpu():
            return "<topology sockets='1' cores='1' threads='1'/>"
        else:
            return "<topology sockets='1' cores='2' threads='1'/>"

    def replace_vcpu(match):
        if is_hygon_cpu():
            return "<vcpu placement='static'>1</vcpu>"
        else:
            return "<vcpu placement='static'>2</vcpu>"

    def replace_name(match):
        return "<name>" + new_vm_domain_id + "</name>"

    def replace_hardware_serials_values(xml_text):
        # Replace serial (12 characters, starts with letter)
        serial_pattern = r'serial=[A-Z][A-Z0-9]{11},'
        new_serial = f'serial={generate_random_string(12)},'
        xml_text = re.sub(serial_pattern, new_serial, xml_text)

        serial_pattern = r'serial=[A-Z0-9]{8},'
        new_serial = f'serial={generate_random_string(8)},'
        xml_text = re.sub(serial_pattern, new_serial, xml_text)

        # Replace uuid with random UUID
        uuid_pattern = r'uuid=[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
        new_uuid = f'uuid={str(uuid.uuid4())}'
        xml_text = re.sub(uuid_pattern, new_uuid, xml_text)

        # Replace part (14 characters + -NVD, starts with letter)
        part_pattern = r'part=[A-Z][A-Z0-9]{13}-NVD'
        new_part = f'part={generate_random_string(14)}-NVD'
        xml_text = re.sub(part_pattern, new_part, xml_text)

        part_pattern = r'part=[A-Z][A-Z0-9]{11}-CWE'
        new_part = f'part={generate_random_string(12)}-CWE'
        xml_text = re.sub(part_pattern, new_part, xml_text)
        return xml_text

    xml_buffer_new = replace_hardware_serials_values(xml_buffer_new)

    if not new_vm_domain_id.startswith("mac"):
        xml_buffer_new = re.sub(
            r"<topology sockets='[0-9]+' dies='[0-9]+' clusters='[0-9]+' cores='[0-9]+' threads='[0-9]+'/>",
            replace_topology,
            xml_buffer_new)
        # 新支点低版本libvirt
        xml_buffer_new = re.sub(
            r"<topology sockets='[0-9]+' dies='[0-9]+' cores='[0-9]+' threads='[0-9]+'/>",
            replace_topology,
            xml_buffer_new)
    if not new_vm_domain_id.startswith("mac"):
        xml_buffer_new = re.sub(r"<vcpu placement='static'>[0-9]+</vcpu>", replace_vcpu, xml_buffer_new)
    xml_buffer_new = re.sub(r"<name>[\w,-]{0,100}</name>", replace_name, xml_buffer_new)
    if is_hygon_cpu():
        xml_buffer_new = re.sub(r"Haswell,-hypervisor",
                                "Westmere-v1,vendor=GenuineIntel,hv_time,hv_relaxed,hv_vapic,hv_spinlocks=0x1fff,kvm=off,hv_vendor_id=xeon",
                                xml_buffer_new)
    else:
        xml_buffer_new = re.sub(r"Haswell,-hypervisor",
                                "Haswell,vendor=GenuineIntel,hv_time,hv_relaxed,hv_vapic,hv_spinlocks=0x1fff,kvm=off,hv_vendor_id=xeon",
                                xml_buffer_new)
    # write out
    with open(new_vm_xml_file_path, "wb+") as fd:
        fd.write(xml_buffer_new.encode())
    return True

def get_disk_dev(xml_file_path_name):
    disk_dev_list = []
    try:
        tree = ET.parse(xml_file_path_name)
        root = tree.getroot()
        for disk in root.findall('./devices/disk'):
            log.debug(disk)
            device = disk.get('device', '')
            source_elem = disk.find('source')
            source_file = source_elem.get('file', '') if source_elem is not None else ''
            target_elem = disk.find('target')
            target_dev = target_elem.get('dev', '') if target_elem is not None else ''
            if device == 'cdrom':
                continue
            elif device != 'disk':
                log.error("unknown disk device: {}, in {}".format(device, xml_file_path_name))
                continue
            log.debug("{} - {}".format(target_dev, source_file))
            disk_info = {'source': source_file, 'dev':target_dev}
            disk_dev_list.append(disk_info)
    except Exception as e:
        log.error("get disk type error from: {}, {}".format(xml_file_path_name, e))
    return disk_dev_list





def _build_vm_bundle_zip(vm_dir):
    """
    根据 vm 目录（包含 windows/ 和 sysmon/），构建一个完整的 VM 初始化 bundle。
    目录结构（host 上）类似：
        vm/
          windows/
            pre_init_env.py
            mof_modify_wmi/
            ohook/
            run_template_win10.json
            run_template_win7x64.json
          sysmon/
            Sysmon_*.exe / Sysmon64_*.exe / xml ...
    打包时：
        - 将 windows/pre_init_env.py 拷贝到临时根目录
        - 将 windows/mof_modify_wmi 拷贝为 根/mof_modify_wmi
        - 将 windows/ohook 拷贝为 根/ohook
        - 将 run_template_win10.json / run_template_win7x64.json 拷贝到根目录
        - 将 sysmon 整个目录拷贝到 根/sysmon
    最终生成 vm_bundle_<pid>_<rand>.zip（放在 vm_dir 下）。
    为避免并发冲突，每次构建使用独立的 _bundle_tmp_<pid>_<rand> 目录和 zip 名。
    """
    vm_dir = os.path.abspath(vm_dir)
    windows_src = os.path.join(vm_dir, "windows")
    sysmon_src  = os.path.join(vm_dir, "sysmon")

    # 每次一个唯一临时目录 + 唯一 zip 文件名，防止并发互相干扰
    rand_suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    bundle_tmp = os.path.join(vm_dir, "_bundle_tmp_%d_%s" % (os.getpid(), rand_suffix))
    bundle_zip_path = os.path.join(vm_dir, "vm_bundle_%d_%s.zip" % (os.getpid(), rand_suffix))

    log.debug("build vm bundle: vm_dir=%s, tmp=%s, zip=%s", vm_dir, bundle_tmp, bundle_zip_path)

    try:
        os.makedirs(bundle_tmp)

        # ---------- 1) 拷贝 sysmon 目录到临时根/sysmon ----------
        if os.path.isdir(sysmon_src):
            sysmon_dst = os.path.join(bundle_tmp, "sysmon")
            shutil.copytree(sysmon_src, sysmon_dst)
            log.debug("copy sysmon: %s -> %s", sysmon_src, sysmon_dst)
        else:
            log.warning("sysmon dir not found: %s", sysmon_src)

        # ---------- 2) 拷贝 windows 相关内容 ----------
        if not os.path.isdir(windows_src):
            log.error("windows dir not found: %s", windows_src)
        else:
            # 2.1 pre_init_env.py 放到 bundle 根（以后在 C:\install 根）
            pre_init_src = os.path.join(windows_src, "pre_init_env.py")
            pre_init_dst = os.path.join(bundle_tmp, "pre_init_env.py")
            if os.path.isfile(pre_init_src):
                shutil.copy2(pre_init_src, pre_init_dst)
                log.debug("copy pre_init_env: %s -> %s", pre_init_src, pre_init_dst)
            else:
                log.error("pre_init_env.py not found: %s", pre_init_src)

            # 2.2 mof_modify_wmi 目录
            mof_src = os.path.join(windows_src, "mof_modify_wmi")
            if os.path.isdir(mof_src):
                mof_dst = os.path.join(bundle_tmp, "mof_modify_wmi")
                shutil.copytree(mof_src, mof_dst)
                log.debug("copy mof_modify_wmi: %s -> %s", mof_src, mof_dst)
            else:
                log.warning("mof_modify_wmi dir not found: %s", mof_src)

            # 2.3 ohook 目录
            ohook_src = os.path.join(windows_src, "ohook")
            if os.path.isdir(ohook_src):
                ohook_dst = os.path.join(bundle_tmp, "ohook")
                shutil.copytree(ohook_src, ohook_dst)
                log.debug("copy ohook: %s -> %s", ohook_src, ohook_dst)
            else:
                log.warning("ohook dir not found: %s", ohook_src)

            # 2.4 模板：run_template_win10.json / run_template_win7x64.json
            for tpl_name in ("run_template_win10.json", "run_template_win7x64.json"):
                tpl_src = os.path.join(windows_src, tpl_name)
                if os.path.isfile(tpl_src):
                    tpl_dst = os.path.join(bundle_tmp, tpl_name)
                    shutil.copy2(tpl_src, tpl_dst)
                    log.debug("copy template: %s -> %s", tpl_src, tpl_dst)
                else:
                    log.warning("template not found: %s", tpl_src)

        # ---------- 3) 打包 zip ----------
        with zipfile.ZipFile(bundle_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(bundle_tmp):
                for name in files:
                    full_path = os.path.join(root, name)
                    if not os.path.exists(full_path):
                        # 极小概率 race，防御一下
                        log.warning("skip missing file during zip: %s", full_path)
                        continue
                    arcname = os.path.relpath(full_path, bundle_tmp)
                    zf.write(full_path, arcname)
                    log.debug("zip add: %s as %s", full_path, arcname)

        log.info("build vm bundle ok: %s", bundle_zip_path)
        return bundle_zip_path
    except Exception:
        log.error("_build_vm_bundle_zip exception: %s", traceback.format_exc())
        raise
    finally:
        # 清理临时目录
        shutil.rmtree(bundle_tmp, ignore_errors=True)

# def _upload_vm_bundle(url_front, domain_id, vm_dirpath=r"C:\install"):
#     """
#     根据当前脚本所在目录下的 vm/ 构建 VM 包并上传到 vm_dirpath。
#     domain_id 目前只用于日志。
#     """
#     bundle_zip_path = None
#     try:
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         vm_dir = os.path.join(current_dir, "vm")
#
#         # 1) 在 host 上构建 bundle zip
#         bundle_zip_path = _build_vm_bundle_zip(vm_dir)
#         if not bundle_zip_path or not os.path.isfile(bundle_zip_path):
#             log.error("_upload_vm_bundle: bundle_zip_path invalid for %s: %r",
#                       domain_id, bundle_zip_path)
#             return False
#
#         # 2) 读 zip 数据
#         with open(bundle_zip_path, "rb") as f:
#             zip_data = f.read()
#
#         # 3) 上传并解压到 vm_dirpath
#         data = {"dirpath": vm_dirpath}
#         r = post_to_vm(
#             url_front,
#             "/extract",
#             files={"zipfile": zip_data},
#             data=data,
#             timeout=300,
#         )
#         if r.status_code != 200:
#             if r.content:
#                 try:
#                     log.debug("extract error: %s", r.json())
#                 except Exception:
#                     log.debug("extract error raw: %r", r.content)
#             return False
#
#         log.info("_upload_vm_bundle ok for %s -> %s", domain_id, vm_dirpath)
#         return True
#
#     except Exception:
#         log.error("_upload_vm_bundle exception for %s: %s", domain_id, traceback.format_exc())
#         return False
#     finally:
#         # 清理临时 zip 文件
#         if bundle_zip_path:
#             try:
#                 os.remove(bundle_zip_path)
#             except Exception:
#                 pass

def upload_pre_init_env(url_front, domain_id):
    """
    通过 agent 将 pre_init_env + sysmon + mof_modify_wmi + ohook 一次性打包上传。
    解压到 C:\\install，随后在 VM 内选择正确的 run_template_*.json 重命名为 run_template.json。
    """
    vm_dirpath = r"C:\install"
    bundle_zip_path = None

    try:
        # 0. 清理 C:\install
        data = {
            "command": r'C:\Windows\system32\cmd.exe /c rmdir /s /q "%s"' % vm_dirpath,
            "cwd": r"C:\\",
        }
        r = post_to_vm(url_front, "/execute", data=data, timeout=40)
        if (r.status_code != 200) and r.content:
            log.debug("rmdir install: %s", r.content)

        # 1. mkdir C:\install
        r = post_to_vm(url_front, "/mkdir", data={"dirpath": vm_dirpath}, timeout=30)
        if (r.status_code != 200) and r.content:
            # 183 = already exists
            if b"[Error 183]" not in r.content:
                log.debug("mkdir install: %s", r.content)

        # 2. 在 host 上构建 vm_bundle_*.zip
        current_dir = os.path.dirname(os.path.abspath(__file__))
        vm_dir = os.path.join(current_dir, "vm")
        bundle_zip_path = _build_vm_bundle_zip(vm_dir)

        # 3. 读 bundle 内容，并通过 /extract 上传 + 解压到 C:\install
        with open(bundle_zip_path, "rb") as f:
            zip_data = f.read()

        data = {"dirpath": vm_dirpath}
        r = post_to_vm(url_front, "/extract", files={"zipfile": zip_data}, data=data)
        if (r.status_code != 200) and r.content:
            log.error("extract vm bundle fail for %s: %s", domain_id, r.content)
        else:
            log.info("extract vm bundle ok for %s", domain_id)

        # 4. 在 VM 内选择合适的模板，复制为 run_template.json
        #    解压后：C:\install\run_template_win10.json / run_template_win7x64.json
        if domain_id.startswith("win10"):
            tpl_name = "run_template_win10.json"
        elif domain_id.startswith("win7"):
            tpl_name = "run_template_win7x64.json"
        else:
            log.info("%s not support template pre init by template yet", domain_id)
            return True  # 不算失败，只是没有模板

        cmd_copy = (
            r'C:\Windows\system32\cmd.exe /c copy /Y '
            r'"%s\%s" "%s\run_template.json"' % (vm_dirpath, tpl_name, vm_dirpath)
        )
        data = {
            "command": cmd_copy,
            "cwd": vm_dirpath,
        }
        r = post_to_vm(url_front, "/execute", data=data, timeout=30)
        if (r.status_code != 200) and r.content:
            log.error("copy run_template.json fail for %s: %s", domain_id, r.content)
        else:
            log.info("set run_template.json ok for %s, tpl=%s", domain_id, tpl_name)

    except Exception:
        log.error("upload pre init env %s exception: %s", domain_id, traceback.format_exc())
        return False
    finally:
        # 清理 host 上临时 zip
        if bundle_zip_path:
            try:
                os.remove(bundle_zip_path)
            except Exception:
                pass

    return True



def random_init_win10(url_front, domain_id):
    """
    在 VM 上执行 pre_init_env.py 的随机初始化逻辑（mode=random）。
    假设 upload_pre_init_env() 已经把 bundle 解压到 C:\\install。
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        vm_dirpath = r"C:\install"

        # 1. 在 VM 上执行 pre_init_env.py -mode=random
        pre_init_env_vm_file_path = vm_dirpath + r"\pre_init_env.py"
        data = {
            "command": r'C:\Python27\pythonw.exe "%s" -mode=random' % pre_init_env_vm_file_path,
            "cwd": vm_dirpath,
        }
        r = post_to_vm(url_front, "/execute", data=data)
        if (r.status_code != 200) and r.content:
            log.debug("exec pre_init_env random for %s: %s", domain_id, r.content)

        # 2. 拉取日志 C:\install\log_pre_init_env.log
        data = {"filepath": vm_dirpath + r"\log_pre_init_env.log"}
        r = post_to_vm(url_front, "/retrieve", data=data, timeout=30)
        log_pre_init_in_host_file_path = os.path.join(
            current_dir, "vm", "windows",
            "%s_log_pre_init_env_random.log" % domain_id
        )
        with open(log_pre_init_in_host_file_path, "wb") as f:
            f.write(r.content)

        log.info(
            "random init win10 done for %s, log=%s",
            domain_id,
            log_pre_init_in_host_file_path,
        )
    except Exception:
        log.error("random_init_win10 %s exception: %s", domain_id, traceback.format_exc())










@add_try_except
def define_domain_create_snapshot(base_image_path, domain_id, ip_address, mac, qemu_kvm_dir):
    start = time.time()
    prefix = domain_id + " "
    current_path = os.path.join(qemu_kvm_dir, domain_id)
    if not os.path.exists(current_path):
        os.mkdir(current_path)

    # CLEAN [1/2] undifine domain
    try:
        returncode, info, error = run_cmd("virsh domstate %s" % (domain_id))
        if not returncode:
            if "shut off" != info.strip():
                returncode, info, error = run_cmd("virsh destroy %s" % (domain_id))
                if returncode:
                    log.error("[FAIL] " + prefix + " destroy domain - %s " % (info, error.replace("\n", " ")))
            if domain_id.startswith("mac"):
                cmd = "virsh undefine --nvram %s --snapshots-metadata " % (domain_id)
            else:
                cmd = "virsh undefine %s --snapshots-metadata " % (domain_id)
            info = os.popen(cmd).read()
            log.info(prefix + " undefine domain - %s " % (info.replace("\n", " ")))
        cmd = "rm -rf {}/*".format(current_path)
        ret, out, err = run_cmd(cmd)
        if ret:
            log.error("[FAIL] {}, {}, {}, {}".format(cmd, ret, out, err))
    except Exception:
        log.info(prefix + " ignore error while undefining domain domain may not exits")

    # CLEAN [1/2] remove qcow2
    current_image_path = os.path.join(current_path, domain_id + ".qcow2")
    if os.path.exists(current_image_path):
        os.remove(current_image_path)
        log.info(prefix + " remove old qcow2 - %s " % (current_image_path))

    # set xml: change mac/files path
    xml_path = os.path.join(current_path, domain_id + "_domain.xml")
    rebuild_clone_xml(base_image_path, xml_path, mac, current_image_path, domain_id)

    clone_disk_cmd = "qemu-img create -f qcow2 -b %s -F qcow2 %s" % (base_image_path, current_image_path)
    returncode, info, error = run_cmd(clone_disk_cmd)
    if returncode:
        log.error(
            "[FAIL] clone disk {} <- {}, info: {}, error: {}".format(current_image_path, base_image_path, info, error))
        return False
    log.info(prefix + "create image - %s -> %d, %s %s" % (
        clone_disk_cmd, returncode, info.replace("\n", "enter"), error.replace("\n", " ")))

    # register vm
    returncode, info, error = run_cmd("virsh define %s" % xml_path)
    if returncode:
        log.error("[FAIL] " + prefix + "define domain - {}, {}".format(info, error))
        return False
    else:
        log.info("[OK] " + prefix + "defined domain")
    # start
    returncode, info, error = run_cmd("virsh start %s" % domain_id)
    if returncode:
        log.error("[FAIL] " + prefix + "start - {}, {}".format(info, error))
        return False
    else:
        log.info("[OK] " + prefix + "start domain - %s start 5 seconds" % (info.replace("\n", " ")))

    time.sleep(5)
    # start
    if domain_id.startswith("win10"):
        for i in range(0, 3):
            dominfo_cmd = "virsh dominfo %s |grep State |awk '{print $NF}'" % (domain_id)
            code, state, error = run_cmd(dominfo_cmd)
            if "running" in state:
                log.info("vm enter running: %s, round: %d, " % (domain_id, i))
                break
            else:
                info = os.popen("virsh start %s" % domain_id).read()
                log.debug("vm not running: " + domain_id + ", %s , wait 10s" % (info.replace("\n", " ")))
                time.sleep(10)

        # reset network mac address and other hardware 只有win10有这个操作 其他会蓝屏卡住
        info = os.popen("virsh reset %s" % domain_id).read()
        log.info("vm reset1 " + prefix + ": %s, wait 20 seconds" % (info.replace("\n", " ")))
    time.sleep(20)
    url = "http://%s:8000" % ip_address
    vm_status = False
    crash = False
    for i in range(0, 3):
        vm_status, crash = wait_for_curl(prefix + " round: " + str(i), url, domain_id)
        if vm_status:
            log.debug(prefix + " first start, wait for curl success")
            break
        else:
            log.info(prefix + " first start, wait for curl crash round %d" % (i))
            # rebuild image
            info = os.popen("virsh destroy %s" % domain_id).read()
            log.info(prefix + "start destroy - %s" % (info.replace("\n", " ")))
            if os.path.exists(current_image_path):
                os.remove(current_image_path)
                log.info(prefix + " remove old qcow2 - %s " % (current_image_path))
            clone_disk_cmd = "qemu-img create -f qcow2 -b %s -F qcow2 %s" % (base_image_path, current_image_path)
            returncode, info, error = run_cmd(clone_disk_cmd)
            log.info(prefix + "create image - %s -> %d, %s %s" % (
                clone_disk_cmd, returncode, info.replace("\n", " "), error.replace("\n", " ")))
            info = os.popen("virsh start %s" % domain_id).read()
            log.info(prefix + "start domain - %s start 5 seconds" % (info.replace("\n", " ")))
            time.sleep(15)
            if domain_id.startswith("win10"):
                # win10 reset network
                for i in range(0, 3):
                    dominfo_cmd = "virsh dominfo %s |grep State |awk '{print $NF}'" % (domain_id)
                    code, state, error = run_cmd(dominfo_cmd)
                    if "running" in state:
                        log.info("vm enter running2: %s, round: %d, " % (domain_id, i))
                        break
                    else:
                        info = os.popen("virsh start %s" % domain_id).read()
                        log.debug("vm not running2: " + domain_id + ", %s , wait 10s" % (info.replace("\n", " ")))
                        time.sleep(10)

            info = os.popen("virsh reset %s" % domain_id).read()
            log.info("vm reset2 " + prefix + ": %s, wait 20 seconds" % (info.replace("\n", " ")))
            time.sleep(20)
    if vm_status == False:
        log.error("[FAIL] " + prefix + "first start domain failed %s. XML config error or base image error. RECHECK", domain_id)
        return False

    run_cmd("chmod a-w %s" % (xml_path))
    set_clock(url)
    # 重启防止win弹窗
    if domain_id.startswith("win"):
        upload_pre_init_env(url, domain_id)
        is_rename_ok = False
        if domain_id.startswith("win10"):
            # init environment for win10
            is_rename_ok = init_env_win10(url, domain_id)
            log.info("rename user name for {}: {}".format(domain_id, is_rename_ok))

        # 重启也会导致死机
        restart_vm(domain_id, prefix)
        time.sleep(20)
        vm_status, crash = wait_for_curl(prefix + "round: " + str(0), url, domain_id)
        if vm_status:
            log.info(prefix + "second start success ")
        else:
            log.warning(prefix + "second start failed.Try to restart!")
            restart_vm(domain_id, prefix)
            vm_status, crash = wait_for_curl(prefix + "_" + str(1) + "_ ", url, domain_id)
            if vm_status:
                log.info(prefix + "second start success ")
            else:
                log.error("[FAIL]" + prefix + " second start failed.CHECK!!")
                return False
        random_init_win10(url, domain_id)
        clean_pre_init_scripts_win10(url, domain_id, is_rename_ok)
    log.debug("waitting 20s before create snapshot: {}".format(domain_id))
    time.sleep(20)
    if domain_id.startswith("win"):
        minimize_show_desktop(url)
    log.debug("Creating snapshot: {}".format(domain_id))
    # create system_clean snapshot
    use_external_snapshot = True
    if use_external_snapshot:
        '''
        virsh snapshot-create-as win10_1903_x64_2016-2 system_clean --live --atomic \
      --memspec file=/data/lsb/qemu_kvm/win10_1903_x64_2016-2/win10_1903_x64_2016-2_memory.dump,snapshot=external \
      --diskspec hda,snapshot=external,file=/data/lsb/qemu_kvm/win10_1903_x64_2016-2/win10_1903_x64_2016-2_run.qcow2
        '''
        disk_dev_list = get_disk_dev(xml_path)
        memory_dump_path = os.path.join(current_path, domain_id + "_memory.dump")
        cmd_snapshot = """virsh snapshot-create-as %s %s --live --atomic \
        --memspec file=%s,snapshot=external \
        """ % (domain_id, "system_clean", memory_dump_path)
        if len(disk_dev_list) == 0:
            log.error("[FAIL] " + prefix + " no disk device found in {}".format(xml_path))
            return False
        for disk_info in disk_dev_list:
            cmd_snapshot += " --diskspec %s,snapshot=external" %(disk_info['dev'])
        returncode, info, error = run_cmd(cmd_snapshot)
        if returncode:
            log.error("fail " + prefix + "create external snapshot - {}; {}. RECHECK!!".format(info, error))
            return False
        else:
            log.info("[OK] " + prefix + "create snapshot")

        run_cmd("chmod a-w %s" % (memory_dump_path))
        for disk_info in disk_dev_list:
            run_cmd("chmod a-w %s" % (disk_info['source']))
    else:
        # use internal snapshot
        returncode, info, error = run_cmd("virsh snapshot-create-as %s --name %s" % (domain_id, "system_clean"))
        if returncode:
            log.error("[FAIL] " + prefix + "create snapshot - {}, {}".format(info, error))
            return False
        else:
            log.info("[OK] " + prefix + "create snapshot")

    info = os.popen("virsh destroy %s" % domain_id).read()
    log.debug(prefix + " destroy - %s" % (info.replace("\n", " ")))
    end = time.time()
    log.info(prefix + "complete node %s %s %s use time %d" % (base_image_path, domain_id, ip_address, end - start))
    return True

def get_diff_disk_by_name(domain_path, domain_id, possible_file_path_name):
    diff_disk = ""
    try:
        if os.path.exists(possible_file_path_name):
            return possible_file_path_name
        base_disk = domain_id + ".qcow2"
        for item_name in os.listdir(domain_path):
            if item_name.endswith((".xml", ".dump", ".bak")):
                continue
            if item_name == base_disk:
                continue
            if "domain_id" not in item_name:
                continue
            item_file_path_name = os.path.join(domain_path, item_name)
            if is_qcow2(item_file_path_name):
                diff_disk += item_file_path_name
    except Exception as e:
        log.error("get diff disk exception: {}".format(e))
    return diff_disk

def get_diff_disk(domain_id):
    diff_disk = ""
    try:
        cmd = "virsh dumpxml %s | grep \"source file\"" %(domain_id)
        retcode, out, err = run_cmd(cmd)
        if retcode:
            log.error("[FAIL] get diff disk fail: {}, out: {}, err: {}".format(retcode, out, err))
            return ""
        base_disk = domain_id + ".qcow2"
        # <source file='/data/lsb/qemu_kvm/win10_1903_x64_2016-45/win10_1903_x64_2016-45.1761814841'/>
        for line in out.splitlines():
            line = line.strip()
            file_path_names = re.findall(r"source file='(.*)'", line)
            if len(file_path_names) < 1:
                log.error("cannot found source file in {} at {}".format(domain_id, line))
                continue
            for path_item in file_path_names:
                basename = os.path.basename(path_item)
                if domain_id not in basename:
                    continue
                elif base_disk == domain_id:
                    continue
                else:
                    diff_disk = path_item
                    log.debug("find diff disk: {}".format(diff_disk))
                    break
            if diff_disk:
                break
    except Exception as e:
        log.error("get diff disk exception: {}".format(e))
    return diff_disk

def is_hygon_cpu():
    try:
        # 调用 lscpu 命令获取 CPU 信息
        result = subprocess.run(['lscpu'], capture_output=True, text=True, check=True)
        cpu_info = result.stdout

        # 检查 CPU 型号是否包含 "Hygon"
        for line in cpu_info.split('\n'):
            if 'Model name' in line:
                cpu_model = line.split(':')[1].strip()
                return "Hygon" in cpu_model
    except Exception as e:
        print(f"Error: {e}")
        return False

    return False


def get_cpu_cores():
    try:
        # 调用 lscpu 命令获取 CPU 信息
        result = subprocess.run(['lscpu'], capture_output=True, text=True, check=True)
        cpu_info = result.stdout

        # 解析输出，提取 CPU(s) 的值
        for line in cpu_info.split('\n'):
            if 'CPU(s):' in line:
                return int(line.split(':')[1].strip())
    except Exception as e:
        print(f"Error: {e}")
        return None


# todo check domain is running if domain just shutdown
@add_try_except
def wait_for_curl(prefix, url, domain_id):
    # wait for ip
    curl_cmd = "curl -s -m 1 %s" % url
    limit = 30
    count = 0
    vm_status = False
    crash = False
    while True:
        count += 1
        code, inf, error = run_cmd(curl_cmd)
        if code == 0:
            log.info("ok agent online: " + prefix)
            vm_status = True
            break
        else:
            log.debug(
                "waiting agent online: " + prefix + " -  count %d" % (count))
        dominfo_cmd = "virsh dominfo %s |grep State |awk '{print $NF}'" % (domain_id)
        code, state, error = run_cmd(dominfo_cmd)
        if "running" in state:
            time.sleep(10)
        else:
            crash = True
            log.info("vm offline: " + prefix + " maybe crash, state: %s" % (state))
            return vm_status, crash

        if count >= limit:
            break
    return vm_status, crash


def network(conf_child_vm_label, source_xml):
    generate_network_xml(source_xml, conf_child_vm_label, "network.xml")
    # redefine network


def deploy(conf_child_vm_label, qemu_kvm_dir, data_dict):
    start = time.time()

    for key, value in conf_child_vm_label.items():
        deploy_vm(key, data_dict, qemu_kvm_dir, value)
    # dep_type="win7_office2013"
    # deploy_vm(dep_type, data_dict, qemu_kvm_dir, conf_child_vm_label[dep_type])
    end = time.time()
    log.info("all complete {}".format(end - start))


def libvirtd_192():
    source_xml = "network_192.xml"
    if not os.path.isfile(source_xml):
        print((source_xml, "not exits"))
        exit(-1)
    id_mac = "id_mac.dat"
    if not os.path.isfile(id_mac):
        print((id_mac, "not exits"))
        exit(-1)
    # network(conf_child_vm_label, source_xml)
    # virsh net-destroy default
    # virsh net-undefine default
    # cp network.xml /etc/libvirt/qemu/network/default.xml
    # virsh net-define /etc/libvirt/qemu/network/default.xml
    # virsh net-start default
    # deploy100(deploy100)
    qemu_kvm_dir = "/data/qemu_kvm"
    for key, value in conf_child_vm_label.items():
        deploy(conf_child_vm_label, qemu_kvm_dir, value)


# virsh list --all |grep shut|awk '{print $2}' |grep "-"|xargs -I {} virsh undefine {}  --snapshots-metadata
if __name__ == '__main__':
    # 创建 ArgumentParser 对象
    username = getpass.getuser();
    if not username == "lsb":
        print("用户错误")
        exit(-1)
    conf_child_vm_label = {}
    parser = argparse.ArgumentParser(description='parse params')
    parser.add_argument('-net', help='网段(100或192)')
    parser.add_argument('-category', help='类型(config,image)')
    parser.add_argument('-label', default="all", help='虚拟机名称(win10_x64_office2016,macos_13_x86_64,...)')
    parser.add_argument('-rename', action="store_true",
                        help='是否重命名计算机名、用户名。是:适用于tmp用户名的管理员账户;否:适用原生用户名')
    args = parser.parse_args()
    if args.net == "100":
        conf_child_vm_label = conf_child_vm_labe_100
    elif args.net == "192":
        conf_child_vm_label = conf_child_vm_label_192
    init_logger()
    if args.net == "100" and args.category == "config":
        source_xml = "onesandbox/network_100.xml"
        if not os.path.isfile(source_xml):
            print((source_xml, "not exits"))
            exit(-1)
        network(conf_child_vm_label, "onesandbox/network_100.xml")
    elif args.net == "192" and args.category == "config":
        source_xml = "onesandbox_192/network_192.xml"
        if not os.path.isfile(source_xml):
            print((source_xml, "not exits"))
            exit(-1)
        network(conf_child_vm_label, source_xml)
    elif args.category == "image":
        mac_map = {}
        qemu_kvm_dir = "/data/lsb/qemu_kvm"
        # load all mac
        for f in os.listdir("./gen"):
            with open("./gen/" + f) as file:
                for line in file.readlines():
                    mac_map[line.split(' ')[0]] = line.split(' ')[1]
        if args.label == "all":
            start = time.time()
            for key, value in conf_child_vm_label.items():
                deploy_vm(key, mac_map, qemu_kvm_dir, value)
            end = time.time()
            log.info("all complete {}".format(end - start))
        else:
            log.debug("args.label: {}".format(args.label))
            deploy_vm(args.label, mac_map, qemu_kvm_dir, conf_child_vm_label[args.label])
    else:
        print("参数错误")

    # virsh net-destroy default
    # virsh net-undefine default
    # cp network.xml /etc/libvirt/qemu/network/default.xml
    # virsh net-define /etc/libvirt/qemu/network/default.xml
    # virsh net-start default
