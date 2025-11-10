/**
 * 这是启动文件
 * @type {{apps: [{name: string, script: string, args: string, interpreter: string, autorestart: boolean, watch: boolean, max_memory_restart: string, log_file: string, log_date_format: string, env: {NODE_ENV: string}, env_production: {NODE_ENV: string}}]}}
 */
module.exports = {
    apps: [
        {
            name: 'ai-photo-editor-backend',
            script: 'uvicorn',

            args: 'main:app --host 0.0.0.0 --port 5015 --workers 2',

            interpreter: 'none',
            autorestart: true,
            watch: false,
            max_memory_restart: '1G',

            log_file: './logs/ai-photo-editor-backend-combined.log',
            log_date_format: 'YYYY-MM-DD HH:mm:ss',

            env: {
                NODE_ENV: 'development',
            },
            env_production: {
                NODE_ENV: 'production',
            }
        }
    ]
};