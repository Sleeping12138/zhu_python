# MySQL查询服务

简单的MySQL数据库查询后端服务

## 安装依赖

```bash
npm install
```

## 启动服务

```bash
npm start
```

## 接口说明

### MySQL查询接口
- **URL**: `POST /api/mysql/search`
- **参数**: 
  ```json
  {
    "sql": "SELECT * FROM table_name LIMIT 10"
  }
  ```
- **返回**:
  ```json
  {
    "code": 200,
    "message": "查询成功",
    "data": [...]
  }
  ```

## 数据库配置

- Host: 121.37.27.174
- User: ai_user
- Password: yishou@666
- Database: world

## 端口

默认端口: 3001