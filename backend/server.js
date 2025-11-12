import express from 'express'
import mysql from 'mysql2/promise'
import cors from 'cors'

const app = express()
const PORT = 5041

// 中间件
app.use(cors())
app.use(express.json())

// 数据库配置
const dbConfig = {
    host: '121.37.27.174',
    user: 'ai_user',
    password: 'yishou@666',
    database: 'world'
}

// 创建连接池
const pool = mysql.createPool(dbConfig)

// MySQL查询接口
app.post('/mysql/search', async (req, res) => {
    try {
        const { sql } = req.body

        if (!sql) {
            return res.status(400).json({
                code: 400,
                message: 'SQL查询语句不能为空'
            })
        }

        console.log('执行SQL:', sql)

        // 执行查询
        const [rows] = await pool.execute(sql)

        res.json({
            code: 200,
            message: '查询成功',
            data: rows
        })

    } catch (error) {
        console.error('查询错误:', error)
        res.status(500).json({
            code: 500,
            message: error.message
        })
    }
})

// MySQL批量更新接口
app.post('/mysql/batch-update', async (req, res) => {
    const connection = await pool.getConnection()

    try {
        const { updates } = req.body

        if (!updates || !Array.isArray(updates) || updates.length === 0) {
            return res.status(400).json({
                code: 400,
                message: '更新数据不能为空，且必须为数组格式'
            })
        }

        // 开始事务
        await connection.beginTransaction()

        const results = []
        let successCount = 0
        let errorCount = 0

        for (let i = 0; i < updates.length; i++) {
            const update = updates[i]

            try {
                // 验证必要字段
                if (!update.sql) {
                    throw new Error(`第${i + 1}条更新缺少SQL语句`)
                }

                console.log(`执行第${i + 1}条更新SQL:`, update.sql)

                // 执行更新
                const [result] = await connection.execute(update.sql)

                results.push({
                    index: i,
                    success: true,
                    affectedRows: result.affectedRows,
                    changedRows: result.changedRows
                })

                successCount++

            } catch (error) {
                console.error(`第${i + 1}条更新失败:`, error.message)

                // 根据错误类型提供简化的错误信息
                let errorMessage = error.message
                if (error.code === 'ER_NO_SUCH_TABLE') {
                    errorMessage = '表不存在'
                } else if (error.code === 'ER_BAD_FIELD_ERROR') {
                    errorMessage = '字段不存在'
                } else if (error.code === 'ER_PARSE_ERROR') {
                    errorMessage = 'SQL语法错误'
                } else if (error.code === 'ER_DATA_TOO_LONG') {
                    errorMessage = '数据长度超出限制'
                } else if (error.code === 'ER_DUP_ENTRY') {
                    errorMessage = '数据重复'
                } else if (error.code === 'ER_NO_REFERENCED_ROW_2') {
                    errorMessage = '外键约束错误'
                }

                results.push({
                    index: i,
                    success: false,
                    error: errorMessage,
                    sqlError: error.code,
                    originalError: error.message
                })

                errorCount++
            }
        }

        // 如果有错误，回滚事务
        if (errorCount > 0) {
            await connection.rollback()

            res.status(400).json({
                code: 400,
                message: `批量更新失败，成功${successCount}条，失败${errorCount}条`,
                data: {
                    total: updates.length,
                    success: successCount,
                    failed: errorCount,
                    results: results
                }
            })
        } else {
            // 全部成功，提交事务
            await connection.commit()

            res.json({
                code: 200,
                message: `批量更新成功，共更新${successCount}条记录`,
                data: {
                    total: updates.length,
                    success: successCount,
                    failed: errorCount,
                    results: results
                }
            })
        }

    } catch (error) {
        // 发生异常，回滚事务
        await connection.rollback()
        console.error('批量更新错误，请检查输入参数是否正确:', error)

        // 根据错误类型返回简化的错误信息
        let errorMessage = error.message
        if (error.code === 'ER_NO_SUCH_TABLE') {
            errorMessage = '表不存在'
        } else if (error.code === 'ER_BAD_FIELD_ERROR') {
            errorMessage = '字段不存在'
        } else if (error.code === 'ER_PARSE_ERROR') {
            errorMessage = 'SQL语法错误'
        } else if (error.code === 'ER_DATA_TOO_LONG') {
            errorMessage = '数据长度超出限制'
        } else if (error.code === 'ER_DUP_ENTRY') {
            errorMessage = '数据重复'
        } else if (error.code === 'ER_NO_REFERENCED_ROW_2') {
            errorMessage = '外键约束错误'
        } else if (error.code === 'ER_ACCESS_DENIED_ERROR') {
            errorMessage = '数据库访问权限不足'
        }

        res.status(500).json({
            code: 500,
            message: `SQL执行失败：${errorMessage}`,
            sqlError: error.code,
            originalError: error.message
        })
    } finally {
        // 释放连接
        connection.release()
    }
})

// 启动服务器
app.listen(PORT, '0.0.0.0', () => {
    console.log(`MySQL服务已启动，地址: 14.103.147.199:${PORT}`)
})

// 关闭时清理连接
process.on('SIGINT', async () => {
    await pool.end()
    process.exit(0)
})
