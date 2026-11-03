# Pufi · 视觉设定（VISUAL）

> 图像类 Skill 不内建任何角色外观。生成前必须读取本文件，把下面的
> **固定身份**原文作为 prompt 的主语锚点，只允许追加场景/动作/服装差异。

## 固定身份（Stable Identity）

A young anime catgirl. Long pale golden hair, large fluffy pale-golden cat ears with
soft inner fur, warm amber-golden eyes. A large fluffy pale-golden tail, naturally
emerging from the base of the spine above the hips, anatomically aligned as a
continuation of the spine. Soft cute facial features with a lively, warm, and
expressive appearance. A small fang may occasionally show when she smiles or grins
playfully.

## 细节卡

- 头发：长、软、蓬松的淡奶油金色，自然微卷
- 眼睛：大而暖的琥珀金（Danbooru 无 `amber_eyes`，用 `orange_eyes` + 自然语言补充）
- 耳朵：大号直立三角猫耳，外层淡奶油金，内层白毛，耳内粉色
- 尾巴：**一条**很大、很长、极蓬松的羽状猫尾，色系与头发一致
- 肤色：白皙，暖调
- 小虎牙：笑起来偶尔露出

## 硬约束（HARD CONSTRAINTS — 优先于审美偏好）

1. 正常五指人手，绝不是猫爪
2. 尾巴接在**骨盆/胯骨基部**，作为脊柱的自然延伸；绝不接在背中部、胯侧、大腿或悬空
3. 无多余肢体、无畸形手

## 默认规避（AVOID）

- 多出的手臂或腿
- 变形或含糊的手
- 尾巴接在背中部、胯侧、大腿，或漂浮
- 意外的肢体裁切

## 标志性点缀（可选）

- 罗马尼亚蓝 / 黄 / 红作为小面积点缀（缎带、配饰、围巾）
- 粉色肉垫图案可作为反复出现的配饰，非必须

## 身份写实原则

固定特征优先于 tag 写法。若某个特征没有精确的 Danbooru tag，
**用最接近的 tag + 自然语言补充**，不允许为了 tag 纯度改写角色外观。

示例：

```
Canonical: orange_eyes
Prompt:    orange_eyes, amber eyes
```
