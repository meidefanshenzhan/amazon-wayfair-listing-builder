# Amazon & Wayfair Listing Builder

一个面向 Amazon 与 Wayfair 的证据驱动型 Listing Skill。它将产品事实、关键词、竞品观察、VOC 和买家问题转化为平台原生文案、结构化字段建议、执行清单与审计结果。

本仓库为私有工作资料。未经仓库所有者书面许可，不得公开、转售、再分发、用于模型训练、提示词蒸馏、自动化抽取或构建实质相似的派生 Skill。

## 适用场景

- 从零搭建 Amazon 或 Wayfair Listing。
- 重写、审核或本地化现有 Listing。
- 将关键词和买家问题映射到正确的平台字段。
- 检查文案中的证据缺口、事实冲突和高风险主张。
- 为 Amazon Alexa/Rufus 或 Wayfair Shop with AI 类型的购物问题建立可回答内容。

本 Skill 不替代完整的市场规模、流量、广告、排名或评论频率分析。竞品页面和评论可以用于发现买家问题，不能证明目标产品的材质、性能、安全、承重、认证或组装体验。

## 安装

将整个仓库复制或克隆到 Codex Skills 目录，并确保目录名称保持为：

```text
amazon-wayfair-listing-builder
```

常见本地位置：

```text
$CODEX_HOME/skills/amazon-wayfair-listing-builder
```

也可以在任务中直接提供该 Skill 的本地目录，并明确要求使用它。

## 调用方式

```text
请使用 amazon-wayfair-listing-builder，为目标产品搭建 Wayfair US Listing。
```

或：

```text
Use amazon-wayfair-listing-builder to audit and rewrite this Amazon US listing.
```

任务中应明确指定平台。Skill 会根据 `amazon` 或 `wayfair` 加载对应的平台规则，不会把 Amazon 字段直接套到 Wayfair，或把 Wayfair 的结构化属性强加给 Amazon。

## 推荐输入

尽量提供以下信息；未知内容应保持未知，不能为了补齐 Listing 而推测：

- 平台、目标站点、语言、类目和产品类型。
- 品牌、型号、SKU、变体关系和每个变体的真实素材。
- 产品尺寸、净重、包装信息、材质、组件、功能和使用边界。
- 组装、清洁、保修、安全、测试和认证资料。
- 当前 Listing（如为优化任务）。
- 关键词及其来源、优先级和日期。
- VOC、评论或买家问题结论及其来源。
- 竞品链接及允许借鉴的维度。
- 需要生成的字段和输出目录。

建议使用脱敏后的结构化摘要，不要上传不必要的原始业务文件。

## 通用工作流

1. 确认平台、类目、语言、产品和变体。
2. 输出输入摘要，区分已验证事实、`DATA_MISSING`、`ASSUMPTION` 和冲突。
3. 生成关键词布局、买家问题库与主张表达表。
4. 按所选平台生成客户可见内容和结构化字段。
5. 生成字段级执行变更与结构化 JSON。
6. 运行确定性审计，并区分现在可执行、等待证据和真正的 P0 发布阻塞项。

## Amazon 输出重点

- Title
- Bullets
- Product Description
- A+ brief（适用时）
- Backend Search Terms（字段存在时）
- Alexa/Rufus 风格的自然语言购物问题覆盖
- ASIN、变体和 Seller Central 字段检查

Amazon 规则见 `references/platform-amazon.md`。

## Wayfair 输出重点

- Product Name
- About This Product
- Features
- What's Included
- Product Dimensions
- Structured Details
- Variation/option mapping
- Image/rich-content brief
- Shop with AI 买家问题覆盖
- 内部 discovery terms（仅在供应商后台存在适用字段时使用）

Wayfair 不默认采用 Amazon 的五点数量、A+、Backend Search Terms 或公开 Q&A 结构。实际字段和限制以当前供应商后台类目模板为准。

Wayfair 规则见 `references/platform-wayfair.md`。

## 输出文件

完整构建通常生成：

```text
product-slug/
├── input_summary.md
├── keyword_placement.md
├── question_library.md
├── claim_expression.md
├── listing_package.md
├── execution_changes.md
├── listing_output.json
└── audit_report.md
```

## 审计

```bash
python scripts/audit_listing.py path/to/listing_output.json --report path/to/audit_report.md
```

JSON 顶层应包含：

```json
{
  "platform": "amazon"
}
```

或：

```json
{
  "platform": "wayfair"
}
```

审计脚本检查字段结构、字符或字节计数、关键词覆盖、声明的证据状态、高风险措辞、问题路由和执行变更。它不能代替平台审核、法律意见、产品测试或人工事实核验。

## 使用示例（脱敏）

```text
请使用 amazon-wayfair-listing-builder，为一个家居收纳产品创建 Wayfair US Listing。

输入包括：
- 已验证的产品规格表与图片；
- 用户提供的关键词优先级；
- 竞品页面和已汇总的 VOC；
- 目标变体清单；
- 平台字段上限由用户提供，但仍需在后台复核。

先输出输入摘要和事实缺口，确认后再生成完整文案、结构化 JSON 与审计报告。
不要编造材质、承重、安全、认证、测试或买家证据。
```

示例故意不包含真实产品、SKU、尺寸、价格、供应商、竞品 URL 或账号数据。

## 隐私保护

- 不要把原始聊天记录、真实姓名、邮箱、电话号码、地址、账号令牌或本地绝对路径提交到仓库。
- 不要提交真实利润表、采购成本、供应商报价、未公开 SKU、测试报告或受限后台导出。
- 提交前使用占位符替换客户名、品牌、ASIN、Wayfair SKU、内部型号和业务指标。
- 只保留完成 Listing 所需的最少证据摘要；原始附件应存放在受控业务系统中。
- 不要把访问令牌写入 remote URL、配置文件、示例或 Git 历史。
- 即使仓库为私有，获准访问的人仍可以克隆并保留本地副本。应定期复核协作者权限。

## 反蒸馏与知识产权保护

- 仓库不保存真实生产案例、原始对话、内部评分集、压力测试提示或逐步推理记录。
- 对外分享时只提供完成工作所需的仓库权限，不共享 GitHub 登录凭据或访问令牌。
- 禁止使用本仓库内容进行模型训练、微调、提示词蒸馏、批量规则抽取或竞品 Skill 复刻，除非仓库所有者书面授权。
- 禁止删除或绕过证据、合规、`DATA_MISSING`、`ASSUMPTION`、`evidence_pending` 和 P0/P1/P2 控制后再分发。
- 私有仓库和文字限制只能降低未经授权使用风险，不能在技术上阻止已获访问者复制内容。敏感方法应遵循最小权限和按需共享原则。

## 协作建议

个人账号下的私有仓库协作者通常拥有写权限。若只希望同事查看，建议将仓库放入 GitHub Organization，并为同事授予 `Read` 角色。撤销权限不会删除对方已经取得的本地副本。

## 权利声明

All rights reserved. No license is granted for public redistribution, commercial resale, model training, fine-tuning, prompt distillation, or creation of substantially similar derivative skills without prior written permission from the repository owner.

