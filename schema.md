# AI SaaS 数据分析项目：数据字典

## 1. 数据表

### orders：订单表

每行代表一条订单记录。

| 字段 | 含义 |
|---|---|
| order_id | 订单唯一标识 |
| user_id | 下单用户 ID |
| product_id | 产品 ID |
| order_date | 订单日期 |
| amount | 订单金额 |
| status | 订单状态 |
| quantity | 购买数量 |

### users：用户表

每行代表一名用户。

| 字段 | 含义 |
|---|---|
| user_id | 用户唯一标识 |
| acquisition_channel | 获客渠道 |
| signup_date | 注册日期 |
| customer_type | 用户类型 |

### products：产品表

每行代表一个产品。

| 字段 | 含义 |
|---|---|
| product_id | 产品唯一标识 |
| product_name | 产品名称 |

注：以上为已使用或此前确认的字段，实际字段全集、数据类型和空值情况以 CSV 文件及 DuckDB DESCRIBE 输出为准。

## 2. 数据表关联

- orders.user_id = users.user_id
- orders.product_id = products.product_id

关联关系：

- users 对 orders：一对多。
- products 对 orders：一对多。

进行关联时应检查维度主键是否唯一、JOIN 是否引起行数放大，以及是否存在未匹配记录。

## 3. 业务指标

**成功支付订单**

status = 'paid'

**总收入（Total Revenue）**

成功支付订单的 amount 总和。

**付费订单数（Paid Orders）**

成功支付订单的数量。

**付费用户数（Paying Users）**

成功支付订单中不同 user_id 的数量。

**ARPPU**

总收入 / 付费用户数。

当付费用户数为 0 时，返回 NULL，不进行除零计算。

**月度指标**

按 order_date 所属自然月统计。

**获客渠道收入**

按照 users.acquisition_channel 分组，计算成功支付订单的收入总和。

## 4. 已验证的数据基线

- orders：240 行
- users：80 行
- products：4 行
- 成功支付订单：184
- 总收入：64,471
- 全期间去重付费用户：72
- 2026 年 4 月收入：31,292

2026 年 4 月渠道收入：

| 渠道 | 收入 |
|---|---:|
| 广告 | 13,656 |
| 自然搜索 | 8,071 |
| 推荐 | 5,579 |
| 直接访问 | 3,986 |

这些结果仅对应当前练习数据集，不应当作其他数据集的通用预期。

## 5. AI SQL 生成规则

1. 只允许使用真实存在且经过授权的表和字段。
2. 使用 DuckDB SQL 语法。
3. 统计收入必须排除非 paid 订单。
4. 根据业务问题确定正确的分组粒度。
5. 日期范围优先采用左闭右开的写法。
6. JOIN 必须使用正确的关联键。
7. 不允许编造数据或查询结果。
8. 当前分析原型仅接受受限的 SELECT 查询。
9. 执行 AI SQL 前必须进行程序级安全检查。
10. 生成业务结论时区分事实、假设和建议，不把相关性直接解释为因果关系。