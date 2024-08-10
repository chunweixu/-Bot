# Ordering-Bot

**Ordering-Bot** 是一个基于LLM与Rasa 框架的智能订餐客服机器人，旨在提供高效的用户服务体验。Ordering-Bot 能够处理用户的菜单请求、订餐、确认订单和信息查询等需求。

## 功能

- **意图识别**：利用自定义的意图识别 Action 来处理各种用户输入。
- **菜单提供**：根据用户请求提供详细的菜单信息。
- **订餐处理**：处理用户的订餐请求，包括菜品和数量的确认。
- **订单确认**：确认用户的订单并提供确认信息。
- **信息查询**：处理用户的其他信息查询请求。

## 项目结构

- `actions.py`: 包含自定义的 Action 类定义，处理意图识别和对话管理。
- `domain.yml`: 定义了意图、动作、响应和槽位。
- `rules.yml`: 定义了对话的规则。
- `stories.yml`: 定义了对话的故事和流程。
- `config.yml`: Rasa 配置文件，包括 NLU 和 Core 的配置。
- `data/`: 存放训练数据，包括 NLU 示例和对话故事。
- `README.md`: 项目的文档说明。

## 安装和运行

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/Ordering-Bot.git
cd Ordering-Bot
```

### 2. 安装依赖

```bash
pip install rasa
```

### 3. 训练模型

运行以下命令以训练 Rasa 模型：

```bash
rasa train
```

### 4. 启动 Action 服务器

在项目目录下，启动 Rasa Action 服务器：

```bash
rasa run actions
```

### 5. 启动 Rasa 服务器

在项目目录下，启动 Rasa 服务器：

```bash
rasa run
```

### 6. 运行对话

你可以通过以下命令启动 Rasa Shell 来与机器人进行对话：

```bash
rasa shell
```