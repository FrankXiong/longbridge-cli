---
name: longbridge-cli
description: 长桥 OpenAPI CLI 工具。查询行情、账户持仓、管理订单、获取市场数据。当用户要求查看长桥账户余额、持仓、下单、撤单、查行情、K线、盘口、资金流向、市场温度时使用此 skill。
metadata: {"clawdbot":{"emoji":"📊","os":["darwin","linux"],"requires":{"bins":["python3"]}}}
---

# 长桥 OpenAPI CLI 工具

通过长桥 OpenAPI 提供行情查询、账户持仓、订单管理、市场数据四大功能模块。

## 环境准备

需设置以下环境变量（可在 `~/.zshrc` 或 `~/.bashrc` 中配置）：

```bash
export LONGBRIDGE_APP_KEY="your_app_key"
export LONGBRIDGE_APP_SECRET="your_app_secret"
export LONGBRIDGE_ACCESS_TOKEN="your_access_token"

# 可选：开启交易权限（默认只读，禁止 buy/sell/cancel）
export LONGBRIDGE_TRADE_ENABLED=true
```

## 安装

**首先检测是否已安装**：

```bash
which longbridge
```

- 若输出路径（如 `/Users/xxx/.local/bin/longbridge`），说明已安装，**跳过以下安装步骤**，直接使用命令。
- 若输出 `longbridge not found`，则按以下步骤安装：

```bash
git clone git@github.com:FrankXiong/longbridge-cli.git
cd longbridge-cli
uv tool install .
```

安装完成后验证：

```bash
longbridge --help
```

## 使用方式

所有命令均支持 `--json` 选项输出 JSON 格式。

### 行情模块

```bash
# 实时报价（支持多个标的）
longbridge quote AAPL.US 700.HK
longbridge quote AAPL.US --json

# 盘口（买5卖5）
longbridge depth 700.HK

# 逐笔成交
longbridge trades 700.HK --count 20

# K 线（period 可选：1m 5m 15m 30m 60m day week month quarter year）
longbridge candlesticks AAPL.US day --count 30
longbridge candlesticks 700.HK 60m --count 100

# 标的静态信息
longbridge info 700.HK AAPL.US
```

### 账户模块

```bash
# 账户余额与净资产
longbridge balance

# 股票持仓
longbridge positions
longbridge positions --json

# 基金持仓
longbridge funds
```

### 订单模块

```bash
# 今日订单（只读，无需交易权限）
longbridge orders

# 历史订单（只读，无需交易权限）
longbridge history-orders --start 2026-01-01 --end 2026-03-14

# 以下命令需设置 LONGBRIDGE_TRADE_ENABLED=true

# 限价买入（会有确认提示，防止误操作）
longbridge buy AAPL.US --qty 100 --price 180.0

# 限价卖出（会有确认提示）
longbridge sell 700.HK --qty 500 --price 320.0

# 撤销订单（会有确认提示）
longbridge cancel 701234567890
```

### 市场数据模块

```bash
# 市场温度（US/HK/CN/SG）
longbridge temperature US
longbridge temperature HK

# 资金流向
longbridge capital-flow 700.HK

# 资金分布（大单/中单/小单）
longbridge capital-dist 700.HK

# 期权链到期日列表
longbridge option-chain AAPL.US
```

## 注意事项

- **下单/撤单命令**：`buy`、`sell`、`cancel` 均有确认提示，确认后才会执行，防止误操作
- **港股代码格式**：使用 4 位 + `.HK` 后缀，如 `0700.HK`、`9988.HK`
- **美股代码格式**：使用股票代码 + `.US` 后缀，如 `AAPL.US`、`NVDA.US`
- **JSON 输出**：所有命令加 `--json` 可输出机器可读的 JSON 格式，便于 AI 解析
- **错误处理**：SDK 异常会输出友好提示，不暴露原始堆栈
