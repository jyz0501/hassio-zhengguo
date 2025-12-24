# Zinguo Bathroom Fan Home Assistant Add-on
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
Zinguo 浴霸 Home Assistant 集成
一个完整的 Zinguo 智能浴霸 Home Assistant 集成。通过用户友好的界面和安全凭证存储，提供对您浴霸的完整控制。

📋 目录

· ✨ 功能特性
· 📦 安装方法
  · 方法一：通过 HACS 安装（推荐）
  · 方法二：Home Assistant 插件方式
  · 方法三：手动安装
· ⚙️ 配置步骤
  · 第一步：添加集成
  · 第二步：输入凭证信息
  · 第三步：完成配置
· 🏠 创建的实体
  · 风扇实体
  · 开关实体
  · 传感器实体
· 🎮 使用方法
  · 风扇控制
  · 独立开关控制
  · 自动化场景
· 🤖 自动化示例
  · 示例1：早晨洗澡预热
  · 示例2：湿度控制
  · 示例3：回家自动预热
  · 示例4：温度保护
· 📱 Lovelace 卡片配置
  · 简洁控制面板
  · 高级控制面板
  · 移动端优化
· 🔧 故障排除
  · 常见问题
  · 错误代码
  · 日志调试
· 🔄 更新与维护
  · 通过 HACS 更新
  · 手动更新
  · 备份配置
· 📊 技术细节
  · API 接口
  · 工作原理
  · 安全机制
· 🤝 参与贡献
  · 报告问题
  · 功能建议
  · 代码贡献
· 📄 许可证
· 🙏 致谢
· 📞 支持与帮助
· 🔗 相关链接

✨ 功能特性

🎛️ 完整的设备控制

· 风扇实体 - 支持预设模式：关闭、吹风、暖风低档、暖风高档
· 独立开关 - 灯光、换气、吹风、暖风1、暖风2 独立控制
· 温度传感器 - 实时温度监测（摄氏度）
· 在线状态 - 设备连接状态实时显示
· 实体分组 - 自动创建设备实体组，便于管理

🔒 安全与隐私保护

· 安全凭证存储 - 使用 Home Assistant 的加密凭证存储
· 本地处理 - 所有数据在本地处理，无云端存储
· 无第三方 - 直接与 Zinguo 官方 API 通信
· 自动令牌刷新 - 自动管理登录令牌，无需手动操作
· 无数据收集 - 不收集任何用户使用数据

🚀 用户体验优化

· 图形化配置 - 完全通过 Web 界面配置，无需编辑 YAML
· 智能错误处理 - 自动重试、网络恢复、错误提示
· 多语言支持 - 支持中文界面显示
· 响应式设计 - 完美适配桌面、平板、手机
· 快速响应 - 控制指令秒级响应

🔄 智能功能

· 状态同步 - 实时同步设备状态
· 场景记忆 - 记住用户偏好设置
· 联动触发 - 支持与其他设备联动
· 定时任务 - 可配置定时开关功能
· 远程控制 - 通过 Home Assistant 远程控制

🛡️ 稳定性保证

· 连接保持 - 自动保持设备连接
· 断线重连 - 网络异常时自动重连
· 状态恢复 - 重启后自动恢复上次状态
· 兼容性强 - 支持多种 Home Assistant 版本
· 更新平滑 - 支持无缝更新

📦 安装方法

方法一：通过 HACS 安装（推荐）

HACS（Home Assistant Community Store）是 Home Assistant 的社区插件商店，提供最便捷的安装方式。

HACS 安装前提

1. 确保已安装 HACS，如果未安装：
   · 访问 HACS 官网
   · 按照教程安装 HACS

安装步骤

1. 打开 HACS
   · 在 Home Assistant 侧边栏点击 HACS
2. 添加自定义仓库
   · 点击 集成
   · 点击右上角 三个点菜单（⋮）
   · 选择 自定义仓库
https://raw.githubusercontent.com/jyz0501/hassio-zinguo/main/images/add-repository.png
3. 填写仓库信息
   ```
   仓库: https://github.com/jyz0501/hassio-zinguo
   类别: 集成
   ```
   · 点击 添加
4. 搜索并安装
   · 在搜索框中输入 Zinguo
   · 点击 Zinguo Bathroom Fan
   · 点击 下载
   · 选择最新版本
   · 点击 下载
https://raw.githubusercontent.com/jyz0501/hassio-zinguo/main/images/install-integration.png
5. 重启 Home Assistant
   · 下载完成后，必须重启 Home Assistant
   · 进入 设置 → 系统
   · 点击 重启

安装验证

· 重启后，检查是否出现 Zinguo Bathroom Fan 集成
· 如果没有出现，尝试清空浏览器缓存

方法二：Home Assistant 插件方式

适合喜欢插件管理的用户，提供更集成的体验。

安装步骤

1. 添加插件仓库
   ```
   仓库地址: https://github.com/jyz0501/hassio-zinguo
   ```
2. 安装插件
   · 在插件商店中搜索 Zinguo Bathroom Fan
   · 点击安装
   · 等待安装完成
3. 配置插件
   · 启动插件
   · 查看日志确保正常运行
4. 重启 Home Assistant
   · 插件安装后需要重启

方法三：手动安装

适合开发者或需要自定义安装的用户。

步骤 1：下载文件

```bash
# 方法 A：使用 Git
git clone https://github.com/jyz0501/hassio-zinguo.git

# 方法 B：下载 ZIP
# 访问 https://github.com/jyz0501/hassio-zinguo/releases
# 下载最新版本的 ZIP 文件
```

步骤 2：解压文件

```bash
# 如果下载的是 ZIP 文件
unzip hassio-zinguo-*.zip

# 进入解压后的目录
cd hassio-zinguo
```

步骤 3：复制文件

1. 打开 Home Assistant 配置目录
2. 创建 custom_components 文件夹（如果不存在）
3. 复制 zinguo 文件夹到 custom_components

目录结构应如下：

```
config/
├── configuration.yaml
├── automations.yaml
├── scenes.yaml
└── custom_components/
    └── zinguo/
        ├── __init__.py
        ├── manifest.json
        ├── config_flow.py
        ├── const.py
        ├── switch.py
        ├── fan.py
        ├── sensor.py
        └── coordinator.py
```

步骤 4：验证安装

1. 重启 Home Assistant
2. 检查日志是否有错误
3. 确认集成出现在列表中

⚙️ 配置步骤

第一步：添加集成

1. 打开集成页面
   · 进入 设置 → 设备与服务
   · 点击 添加集成（右下角）
2. 搜索集成
   · 在搜索框中输入 Zinguo
   · 选择 Zinguo Bathroom Fan
https://raw.githubusercontent.com/jyz0501/hassio-zinguo/main/images/add-integration.png
3. 开始配置
   · 点击集成名称开始配置
   · 系统会显示配置向导

第二步：输入凭证信息
在配置页面中，需要填写以下信息：

字段 说明 示例 必填
账户 注册 Zinguo 应用时使用的手机号
密码 Zinguo 账户的密码 
MAC 地址 浴霸设备的 MAC 地址
名称 自定义设备名称 主卫浴霸

如何获取 MAC 地址？

1. 打开 Zinguo 官方 App
2. 进入设备详情页面
3. 查看设备信息中的 MAC 地址
4. MAC 地址应为 12位大写字母数字，无冒号或短横线

注意事项

· 账户密码会安全加密存储，不会明文显示
· MAC 地址必须完全匹配，包括大小写
· 设备名称会用于创建所有实体的前缀

第三步：完成配置

1. 提交配置
   · 填写完所有信息后点击 提交
   · 系统会验证账户和设备信息
2. 验证成功
   · 如果信息正确，会显示配置成功
   · 系统会自动创建所有实体
3. 配置选项
   · 完成配置后，可以点击集成的 选项 进行修改
   · 可以修改设备显示名称

🏠 创建的实体

成功配置后，系统会自动创建以下实体：

风扇实体

· 实体ID: fan.[设备名称]_fan
· 名称: [设备名称] Fan
· 功能: 主控制面板，包含所有预设模式
· 状态: 开关状态、预设模式
· 属性: 温度、在线状态等

开关实体

灯光开关

· 实体ID: switch.[设备名称]_light
· 名称: [设备名称] Light
· 功能: 控制浴霸灯光
· 图标: mdi:lightbulb

换气开关

· 实体ID: switch.[设备名称]_ventilation
· 名称: [设备名称] Ventilation
· 功能: 控制换气功能
· 图标: mdi:air-filter

吹风开关

· 实体ID: switch.[设备名称]_wind
· 名称: [设备名称] Wind
· 功能: 控制吹风功能
· 图标: mdi:fan

暖风1开关

· 实体ID: switch.[设备名称]_heater_1
· 名称: [设备名称] Heater 1
· 功能: 控制暖风1（低档加热）
· 图标: mdi:radiator

暖风2开关

· 实体ID: switch.[设备名称]_heater_2
· 名称: [设备名称] Heater 2
· 功能: 控制暖风2（高档加热）
· 图标: mdi:radiator

传感器实体

温度传感器

· 实体ID: sensor.[设备名称]_temperature
· 名称: [设备名称] Temperature
· 单位: °C
· 精度: 0.1°C
· 设备类: temperature
· 更新频率: 5分钟

在线状态传感器

· 实体ID: sensor.[设备名称]_online_status
· 名称: [设备名称] Online Status
· 状态值: Online / Offline / Unknown
· 功能: 显示设备连接状态

设备注册

所有实体都会自动注册到同一个设备下：

· 设备名称: 您在配置时设置的名称
· 制造商: Zinguo
· 型号: Smart Bathroom Fan
· 连接方式: 云端

🎮 使用方法

风扇控制

风扇实体提供了完整的预设模式控制：

可用模式

1. off - 关闭所有功能
2. cool - 吹风模式（仅吹风）
3. heat_low - 暖风低档（暖风1 + 吹风）
4. heat_high - 暖风高档（暖风2 + 吹风）

控制方式

```yaml
# 开启吹风模式
service: fan.set_preset_mode
target:
  entity_id: fan.bathroom_fan
data:
  preset_mode: "cool"

# 开启暖风低档
service: fan.set_preset_mode
target:
  entity_id: fan.bathroom_fan
data:
  preset_mode: "heat_low"

# 关闭风扇
service: fan.turn_off
target:
  entity_id: fan.bathroom_fan
```

独立开关控制

除了风扇实体，您还可以单独控制每个功能：

```yaml
# 打开灯光
service: switch.turn_on
target:
  entity_id: switch.bathroom_light

# 打开换气
service: switch.turn_on
target:
  entity_id: switch.bathroom_ventilation

# 打开暖风1
service: switch.turn_on
target:
  entity_id: switch.bathroom_heater_1
```

自动化场景

场景1：洗澡前预热

```yaml
automation:
  - alias: "洗澡前预热"
    trigger:
      - platform: time
        at: "19:30:00"
    condition:
      - condition: time
        weekday:
          - mon
          - tue
          - wed
          - thu
          - fri
          - sat
          - sun
    action:
      - service: fan.set_preset_mode
        target:
          entity_id: fan.bathroom_fan
        data:
          preset_mode: "heat_low"
```

场景2：自动换气

```yaml
automation:
  - alias: "湿度高时自动换气"
    trigger:
      platform: numeric_state
      entity_id: sensor.bathroom_humidity
      above: 80
      for:
        minutes: 5
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.bathroom_ventilation
      - delay:
          minutes: 30
      - service: switch.turn_off
        target:
          entity_id: switch.bathroom_ventilation
```

🤖 自动化示例

示例1：早晨洗澡预热

这个自动化会在工作日早晨自动预热卫生间：

```yaml
automation:
  - alias: "工作日早晨预热"
    description: "工作日7点自动开启暖风"
    trigger:
      platform: time
      at: "07:00:00"
    condition:
      condition: time
      weekday:
        - mon
        - tue
        - wed
        - thu
        - fri
      condition: state
      entity_id: sensor.bathroom_temperature
      below: 22
    action:
      - service: fan.set_preset_mode
        target:
          entity_id: fan.bathroom_fan
        data:
          preset_mode: "heat_low"
      - delay:
          minutes: 20
      - service: fan.set_preset_mode
        target:
          entity_id: fan.bathroom_fan
        data:
          preset_mode: "off"
    mode: single
```

示例2：湿度控制

根据卫生间湿度自动开启换气：

```yaml
automation:
  - alias: "智能湿度控制"
    description: "湿度超过75%自动换气"
    trigger:
      - platform: numeric_state
        entity_id: sensor.bathroom_humidity
        above: 75
      - platform: state
        entity_id: binary_sensor.bathroom_motion
        to: "off"
        from: "on"
    condition:
      - condition: state
        entity_id: switch.bathroom_ventilation
        state: "off"
      - condition: template
        value_template: >
          {{ states('sensor.bathroom_humidity') | float > 75 }}
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.bathroom_ventilation
      - delay:
          minutes: 25
      - service: switch.turn_off
        target:
          entity_id: switch.bathroom_ventilation
    mode: restart
```

示例3：回家自动预热

配合地理位置传感器，回家前自动预热：

```yaml
automation:
  - alias: "回家自动预热"
    description: "检测到即将回家时预热卫生间"
    trigger:
      platform: zone
      entity_id: device_tracker.person_name
      zone: zone.home
      event: enter
    condition:
      condition: sun
      after: sunset
      before: sunrise
      condition: template
      value_template: >
        {{ states('sensor.bathroom_temperature') | float < 20 }}
    action:
      - service: fan.set_preset_mode
        target:
          entity_id: fan.bathroom_fan
        data:
          preset_mode: "heat_low"
      - delay:
          minutes: 15
      - service: fan.set_preset_mode
        target:
          entity_id: fan.bathroom_fan
        data:
          preset_mode: "off"
```

示例4：温度保护

防止浴霸过热，设置温度保护：

```yaml
automation:
  - alias: "温度保护"
    description: "温度过高时自动关闭加热"
    trigger:
      platform: numeric_state
      entity_id: sensor.bathroom_temperature
      above: 35
    condition:
      condition: or
      conditions:
        - condition: state
          entity_id: switch.bathroom_heater_1
          state: "on"
        - condition: state
          entity_id: switch.bathroom_heater_2
          state: "on"
    action:
      - service: fan.set_preset_mode
        target:
          entity_id: fan.bathroom_fan
        data:
          preset_mode: "off"
      - service: notify.mobile_app_phone
        data:
          message: "浴霸温度过高，已自动关闭加热功能"
          title: "安全提醒"
    mode: single
```

📱 Lovelace 卡片配置

简洁控制面板

创建一个简洁的控制面板：

```yaml
type: vertical-stack
cards:
  - type: entity
    entity: fan.bathroom_fan
    name: 浴霸控制
    icon: mdi:fan
    tap_action:
      action: more-info
  - type: horizontal-stack
    cards:
      - type: button
        entity: switch.bathroom_light
        name: 灯光
        icon: mdi:lightbulb
        tap_action:
          action: toggle
      - type: button
        entity: switch.bathroom_ventilation
        name: 换气
        icon: mdi:air-filter
        tap_action:
          action: toggle
  - type: entities
    entities:
      - entity: sensor.bathroom_temperature
        name: 当前温度
        icon: mdi:thermometer
      - entity: sensor.bathroom_online_status
        name: 设备状态
        icon: mdi:wifi
```

高级控制面板

创建更高级的控制面板：

```yaml
type: custom:mushroom-title-card
title: 卫生间浴霸
subtitle: Zinguo 智能浴霸

type: custom:mushroom-chips-card
chips:
  - type: template
    icon: mdi:fan
    icon_color: |
      [[[
        if (states['fan.bathroom_fan'].state === 'off')
          return 'grey';
        else
          return 'blue';
      ]]]
    content: |
      [[[
        const state = states['fan.bathroom_fan'].state;
        if (state === 'off') return '关闭';
        if (state === 'cool') return '吹风';
        if (state === 'heat_low') return '暖风低档';
        if (state === 'heat_high') return '暖风高档';
        return state;
      ]]]
    tap_action:
      action: more-info
      entity: fan.bathroom_fan

type: custom:mushroom-template-card
primary: 温度
secondary: |
  [[[ return states['sensor.bathroom_temperature'].state + '°C'; ]]]
icon: mdi:thermometer
icon_color: |
  [[[
    const temp = parseFloat(states['sensor.bathroom_temperature'].state);
    if (temp < 20) return 'blue';
    if (temp > 30) return 'red';
    return 'green';
  ]]]

type: custom:mushroom-entity-card
entity: sensor.bathroom_online_status
name: 连接状态
icon: mdi:wifi
icon_color: |
  [[[
    if (states['sensor.bathroom_online_status'].state === 'Online')
      return 'green';
    else
      return 'red';
  ]]]
```

移动端优化

为手机优化的卡片：

```yaml
type: custom:layout-card
layout_type: custom:grid-layout
layout:
  grid-template-columns: 1fr 1fr
  grid-template-rows: auto
  grid-gap: 12px
cards:
  - type: custom:button-card
    entity: fan.bathroom_fan
    name: 主控制
    icon: mdi:fan
    state:
      - value: 'off'
        color: grey
      - value: 'cool'
        color: blue
        icon: mdi:fan
      - value: 'heat_low'
        color: orange
        icon: mdi:radiator
      - value: 'heat_high'
        color: red
        icon: mdi:radiator
    tap_action:
      action: more-info
    hold_action:
      action: more-info
      
  - type: custom:button-card
    entity: switch.bathroom_light
    name: 灯光
    icon: mdi:lightbulb
    tap_action:
      action: toggle
      
  - type: custom:button-card
    entity: switch.bathroom_ventilation
    name: 换气
    icon: mdi:air-filter
    tap_action:
      action: toggle
      
  - type: custom:button-card
    entity: sensor.bathroom_temperature
    name: 温度
    unit: °C
    icon: mdi:thermometer
    color_type: card
    color: |
      [[[
        const temp = parseFloat(entity.state);
        if (temp < 20) return 'blue';
        if (temp > 30) return 'red';
        return 'green';
      ]]]
```

🔧 故障排除

常见问题

Q1: 集成安装后没有出现在集成列表中

可能原因：

1. 没有重启 Home Assistant
2. 文件复制位置错误
3. 文件权限问题

解决方法：

1. 确保已重启 Home Assistant
2. 检查 custom_components/zinguo 文件夹是否存在
3. 检查文件权限：chmod -R 755 config/custom_components/zinguo
4. 查看 Home Assistant 日志：tail -f config/home-assistant.log

Q2: 配置时提示"无法连接到设备"

可能原因：

1. MAC 地址错误
2. 账户密码错误
3. 设备不在线
4. 网络问题

解决方法：

1. 确认 MAC 地址（12位大写字母数字）
2. 用 Zinguo App 测试账户密码
3. 检查设备是否在线
4. 检查网络连接

Q3: 实体状态不更新

可能原因：

1. 设备离线
2. API 令牌过期
3. 网络不稳定

解决方法：

1. 检查在线状态传感器
2. 重启集成（删除后重新添加）
3. 检查网络连接

Q4: 控制指令执行失败

可能原因：

1. 设备未响应
2. API 限制
3. 并发控制

解决方法：

1. 等待几秒后重试
2. 检查设备是否繁忙
3. 不要频繁发送指令

错误代码

错误代码 含义 解决方法
401 认证失败 重新输入账户密码
404 设备未找到 检查 MAC 地址
500 服务器错误 等待后重试
timeout 连接超时 检查网络连接
invalid_token 令牌无效 重启集成

日志调试

启用调试日志以获取详细信息：

```yaml
# 在 configuration.yaml 中添加
logger:
  default: info
  logs:
    custom_components.zinguo: debug
```

查看日志：

```bash
# SSH 登录到 Home Assistant
tail -f config/home-assistant.log | grep zinguo

# 或通过 Web 界面
设置 → 系统 → 日志
```

🔄 更新与维护

通过 HACS 更新

1. 打开 HACS → 集成
2. 找到 Zinguo Bathroom Fan
3. 如果有更新可用，会显示 更新 按钮
4. 点击更新，选择版本
5. 下载完成后重启 Home Assistant

手动更新

1. 备份当前配置
2. 下载最新版本
3. 替换 custom_components/zinguo 文件夹
4. 重启 Home Assistant

备份配置

建议定期备份：

```bash
# 备份集成配置
tar -czf zinguo-backup-$(date +%Y%m%d).tar.gz \
  config/custom_components/zinguo \
  config/.storage/core.config_entries
```

📊 技术细节

API 接口

本集成使用 Zinguo 官方 API：

认证接口

· URL: https://iot.zinguo.com/api/v1/customer/login
· 方法: POST
· 参数: {"account":"手机号","password":"密码"}

设备状态查询

· URL: https://iot.zinguo.com/api/v1/customer/devices
· 方法: GET
· 头部: x-access-token: [令牌]

设备控制

· URL: https://iot.zinguo.com/api/v1/wifiyuba/yuBaControl
· 方法: PUT
· 头部: x-access-token: [令牌]
· 参数: 包含设备 MAC 和控制指令的 JSON

工作原理

1. 认证阶段：使用账户密码获取访问令牌
2. 设备发现：查询账户下所有设备，按 MAC 地址匹配
3. 状态轮询：每5分钟查询一次设备状态
4. 控制指令：发送控制指令并立即刷新状态
5. 错误处理：令牌过期时自动重新认证

安全机制

1. 凭证安全：密码使用 Home Assistant 加密存储
2. 令牌管理：令牌存储在内存中，不持久化
3. 通信加密：所有 API 调用使用 HTTPS
4. 本地处理：所有数据在本地处理
5. 权限控制：遵循 Home Assistant 权限系统

🤝 参与贡献

欢迎参与项目开发！

报告问题

发现 bug 或有疑问？

1. 访问 GitHub Issues
2. 点击 New Issue
3. 选择问题类型
4. 提供详细信息：
   · Home Assistant 版本
   · 集成版本
   · 错误日志
   · 复现步骤

功能建议

有新功能想法？

1. 创建 Feature Request Issue
2. 描述功能需求
3. 说明使用场景
4. 如果有，提供参考实现

代码贡献

想要贡献代码？

1. Fork 本仓库
2. 创建功能分支
3. 提交代码变更
4. 创建 Pull Request

代码规范：

· 遵循 Python PEP 8
· 添加类型注解
· 编写文档注释
· 包含测试用例

📄 许可证

本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情。

MIT 许可证赋予您以下权利：

· 自由使用、复制、修改、合并、出版发行、再授权及销售软件及软件的副本
· 在软件和软件的所有副本中都必须包含版权声明和许可声明

🙏 致谢

感谢以下人员和项目：

· Zinguo - 提供优质的智能浴霸产品
· Home Assistant 团队 - 创建了优秀的智能家居平台
· HACS 团队 - 提供了便捷的插件管理
· 所有贡献者 - 感谢代码贡献和问题反馈
· 测试用户 - 感谢早期测试和反馈

📞 支持与帮助

获取帮助

1. GitHub Issues - 报告问题和功能请求
2. Home Assistant 社区 - 在论坛中寻求帮助
3. Discussions - 参与功能讨论

联系维护者

· GitHub: @jyz0501
· Email: 通过 GitHub 个人资料获取

捐赠支持

如果您觉得这个项目对您有帮助，可以考虑：

1. Star 项目 - 给项目点个星
2. 分享推荐 - 推荐给其他 Home Assistant 用户
3. 参与开发 - 贡献代码或文档
4. 报告反馈 - 帮助改进项目

🔗 相关链接

官方链接

· Home Assistant 官网
· HACS 官网
· Zinguo 官网

社区资源

· Home Assistant 中文社区
· Home Assistant 官方论坛
· Home Assistant Discord

相关项目

· Home Assistant Core
· HACS
· Awesome Home Assistant

学习资源

· Home Assistant 入门指南
· Home Assistant 自动化教程
· Lovelace UI 配置

---

感谢使用 Zinguo 浴霸 Home Assistant 集成！

如果这个项目对您有帮助，请考虑：

1. ⭐ 给项目 Star - 让更多人看到
2. 📢 分享给朋友 - 帮助更多用户
3. 🐛 报告问题 - 帮助改进质量
4. 💡 提出建议 - 共同完善功能

祝您使用愉快！🚿✨