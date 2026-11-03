# Pufi Lorebook 素材全面分析（NSFW included）

---

## 0. 勘误

已确认：
- 四本 lorebook 完整读取完毕，未遗漏任何 entry。
- 以下分析包含并正视所有 NSFW 内容。NSFW 是核心素材，后续出图直接使用。
- 文件来源：SillyTavern RISUGAI lorebook 格式（`entries` dict，每 entry 有 `key/selective/content/metadata`）。

---

## A. 四本 Lorebook 逐本分析

### A1. `0517女性服饰、丝袜、高跟鞋穿着指导.json`

| 维度 | 内容 |
|------|------|
| 格式 | RISUGAI lorebook，7 entries，纯视觉效果写作指导 |
| 可用 entries | **全部 7 个**（无 disable） |

**每 entry 分析：**

| entry | comment | 图像价值 | 说明 |
|-------|---------|----------|------|
| 0 | 底层防火墙与前置拦截系统 | 低 | 全是种族/年龄/肤色过滤规则，不出图，可忽略 |
| 1 | 舞台搭建与材质加载 | 中 | 材质词汇（布料、纹样、蕾丝、暗纹），世界观对应材质库 |
| 2 | 高级静态视觉装配与平滑运镜 | **高** | 详细的衣着视觉装配流程（领口→肩带→袖口→裙摆→开叉→饰品），相当于 image composition 指南 |
| 3 | 动态演出与感官爆发滤镜 | **高** | 步态动态（猫步、足音、重心）、丝袜光泽动态、光线折射、脚趾蜷缩等细节 — 这些直接对应 image 的 pose 和细节 prompt |
| 4 | 终极禁令（防过拟合） | 无 | 仅写作规则，不出图 |
| 5 | 思维链 COT | 中 | 提供 visual assembly 的 step 框架，可转化为 composition logic |
| 6 | 缝入思维链 COT | 中 | 同上，更详细 |

**可提取的视觉素材类型：**
- 材质词汇：天蚕丝、重工蕾丝、薄纱、缎面、漆面PU、丝绒、绸缎
- 鞋款词汇：尖头细高跟、酒杯跟、玛丽珍、一字带凉鞋、透明水晶鞋、绑带凉鞋
- 丝袜视觉：5D-50D 透明度梯度、油亮反光、纯色/渐变/渔网/蕾丝拼接、脚尖强化/分趾
- 步态动态：腰肢扭转、裙摆波浪、猫步节奏、足音清脆/沉重
- 光线交互：顺光反射、侧光聚光、行走光泽滑动、膝窝阴影、脚踝收束
- 张力细节：丝袜边缘勒肉、布料紧绷横纹、脚趾蜷缩、微表情联动

---

### A2. `be4863ebb2a69c0e.json`

| 维度 | 内容 |
|------|------|
| 格式 | RISUGAI lorebook，7 entries，**全部 disable: true** |
| 内容类型 | NSFW 古典文风合集 — 纯写作风格指南，非素材库 |

**每 entry 分析：**

| entry | comment | 图像价值 | 说明 |
|-------|---------|----------|------|
| 50112 | 服装描写强化 | **中～高** | 提供了"整体定调→容貌神态→上衣→裸露→下装→足部"的**视觉描写流程**，可直接作为 image composition 流程。带具体示例。 |
| 219644 | 道家美母（旧） | 中 | 提供**古典仙侠审美词汇**（凝脂赛雪、螓首蛾眉、云鬓、莲步）、场景概念（道观、烛光、纱帐、月光），以及"古典环境 + 肉体反差"的视觉框架。但语言是写作指令。 |
| 273185 | 反差婊强化 | **低** | 角色行为心理学，极少视觉描写。 |
| 300664 | 恋物文风 | **中～高** | **高密度视觉词汇**：工笔女性身体描写、服饰恋物级精细刻画（丝袜旦数、跟高、面料质感、款式细节）、古典与色情的视觉融合。大量具象描写。 |
| 527389 | 文言母猪 | 中 | **名物堆叠词汇**（紫檀/螺钿/缂丝/玳瑁/藻井/琉璃/沉香/鎏金 — 环境器物），**服饰词汇**（肚兜/罗裙/绡纱/步摇/珠钗），以及"烛光窥探"的场景光线美学（烛火/水面反光/透窗月色/纱帐/轻烟）。但包裹在 NSFW 写作指令中。 |
| 833460 | 反差文风 | 中 | 大量的具体**外貌描写示例**（清纯少女汉服、浓妆熟妇、换装细节），可拆出 outfit/expression 素材。 |
| 324298 | 声明 | 无 | 仅致谢 |

**可提取的视觉素材类型（需手动提取）：**
- 古典环境词汇：洞府、道观、烛光纱帐、紫檀屏风、鎏金香炉、螺钿床榻
- 服饰名词：肚兜、罗裙、绡纱、云肩、步摇、珠钗、璎珞、荷包
- 中国风色彩：墨绿、藕荷、月白、水蓝、鸦青、银红、蜜合
- 视觉比喻："满月般的肥臀"、"玉脂般的欣长美腿"、"天鹅般优雅的秀颈"
- 光线场景：烛光暖黄、窗格月光、水面反光、香炉轻烟
- 动态细节：布料勒肉、走路臀浪、裙摆翻飞

> ⚠️ **关键限制**：be4863 全部是 disable: true，意味在 SillyTavern 中默认不激活。所有素材需手工提取。

---

### A3. `cloth_lorebook520-522.json`

| 维度 | 内容 |
|------|------|
| 格式 | RISUGAI lorebook，14 entries，**大部分 selective: true** |
| 内容类型 | 服装设计元素库 + 情趣服装目录 |

**每 entry 分析：**

| entry | comment | disable | 图像价值 | 说明 |
|-------|---------|---------|----------|------|
| 2 | 女性内衣设计元素-通用库 | ❌ | **极高** | 完整的材质/结构/工艺/色彩分类：罩杯类型、肩带、后背设计、边缘、材质（丝绸/雪纺/薄纱/网纱/缎面/冰丝）、光线效果、装饰元素。可当 outfit design kit。 |
| 3 | 女性丝袜设计元素-通用库 | ❌ | **极高** | 完整的丝袜分类（连裤袜/吊带袜/大腿袜/过膝袜/渔网袜/油亮袜），丹数规格（5D-120D），结构细节（裆部/脚尖/防滑带），光泽分类（高光油亮→丝滑柔光→半哑光→天鹅绒哑光），图案和色彩体系 |
| 4 | 女性高跟鞋设计元素-通用库 | ❌ | **极高** | 完整的设计体系：鞋头形状、鞋口、鞋跟（细高跟/针形/锥形/粗跟/猫跟/异形跟）、材质（漆面PU/缎面/丝绒/透光树脂）、装饰、色彩、光影行为、声音、步态、姿态心理。可直接当鞋类 prompt 参考。 |
| 5 | 瑜伽裤 | ❌ | 高 | 瑜伽服/运动服设计分类，分色情/非色情两类。材质（裸感尼龙/哑光/亮面/冰丝），动态效果（深蹲臀线拉伸、猫式背部勒紧、前屈腰窝阴影）。 |
| 7-10 | 情趣服装四分类 | ❌ | **极高** | **四大类数百套 outfit 概念**：网纱/透明连体类、皮革/束缚/链条类、蕾丝/缎面/丝绸类、cosplay 职业类。每个都是完整的 outfit 设计概念，带材质/结构/镂空位置/装饰细节。可以直接作为 Pufi illustration 的衣装 source。 |
| 11 | 动物/幻想角色类 | ✅ disable | **高** | 兔女郎、猫女皮装、天使、恶魔、独角兽、美人鱼、精灵、龙女、狐妖 等 25+ fantasy outfit 概念。适配 Pufi 的猫娘身份尤其合适。 |
| 12 | 极简/装饰暴露类 | ❌ | 中 | 超极简装饰类 outfit（珍珠串、链条、金叶、水晶贴饰等）— 适合特定 NSFW 场景 |

**可提取的核心价值：**
- **款式 + 材质 + 色彩**的三元 outfit 设计库，可直接组合生成 infinite outfit concepts
- 精细度足够直接写进 image prompt
- 动态效果描述（布料随动作的光泽/褶皱/拉伸变化）
- 幻想/cosplay 分类与 Pufi 角色高度兼容

---

### A4. `nai4-tti-lorebook.json`

| 维度 | 内容 |
|------|------|
| 格式 | RISUGAI lorebook，4 entries，`outletName: img-gen` |
| 内容类型 | 文生图提示词生成规则 |

**每 entry 分析：**

| entry | comment | disable | 图像价值 | 说明 |
|-------|---------|---------|----------|------|
| 0-1 | 开始/结束 | ❌ | — | XML wrapper |
| 4 | 性姿势 | ✅ | 中 | 数百个 NSFW pose/action tags（doggystyle, missionary, fellatio, cum, bdsm, group 等）— 纯粹 is NSFW tag list |
| 7 | tti | ❌ | **极高** | **完整 image prompt 生成框架**：Scene Composition（人物数量+环境+时间+位置+镜头），Character Prompt（名称格式、人物特点、饰品、职业、姿势、动作细节、衣物细节、人物交互）。带多个完整示例。可直接作为 prompt 模板使用。 |

**可提取的核心价值：**
- **Prompt 模板**：`[img-gen] Scene Composition: ...; Character Prompt: ...; [/img-gen]`
- 构图要素：人物构成（1girl, 2girls, 1boy 等）、环境（indoor/outdoor/beach/bedroom）、时间（morning/night/evening）、镜头（lower_body/from_above/pantyshot/looking_at_viewer）
- 人物描述结构：gender → age → outfit → hair → eyes → expression → pose → action
- 交互语法：`{source#action}` / `{target#action}` 表示角色间接触

---

## B. 综合素材覆盖评估

| 维度 | 覆盖 | 来源 | 质量 |
|------|------|------|------|
| **outfit** | ✅ 充足 | cloth 全分类 + 0517 鞋/袜 + be4863 古典服饰 + 情趣/cosplay | **极高** |
| **footwear/hosiery** | ✅ 极丰富 | 0517 + cloth[3][4] 完整体系 | **极高** |
| **lingerie/fetish** | ✅ 极丰富 | cloth[2][7-12] 全覆盖 | **极高** |
| **fantasy/AU outfit** | ✅ 充足 | cloth[11] 动物/幻想 + be4863 古典仙侠 | 高 |
| **composition/prompt** | ✅ 可用 | nai4[7] 框架 + 0517[2][5] 运镜 | 中高 |
| **lighting/atmosphere** | △ 中等 | be4863 烛光/月光/纱帐 + cloth 光泽体系 + 0517 动态光泽 | 中 |
| **pose/action** | △ NSFW 充足/SFW 弱 | nai4[4] 大量性姿势 tags + 0517[3] 步态 + pufi.md 猫动作 | **NSFW 极高**，SFW 缺 |
| **mood/expression** | ❌ 缺失 | pufi.md 有情绪状态但无 visual mood 词汇 | 低 |
| **environment/scene** | ❌ 缺失 | be4863 仅有古典环境 + cloth 无环境 | 低 |
| **daily life / work** | ❌ 缺失 | 无 lorebook 涉及 | 无 |
| **travel/outdoor** | ❌ 缺失 | 无 lorebook 涉及 | 无 |
| **season/weather** | ❌ 缺失 | 无 lorebook 涉及 | 无 |

---

## C. 最小运行时素材组织方式

基于实际内容，不建议提前设计 schema。当前最合理的做法：

```json
{
  "version": 1,
  "sources": {
    "cloth_lorebook": "cloth_lorebook520-522.json",
    "hosiery_fashion": "0517女性服饰...json",
    "classical_aesthetic": "be4863ebb2a69c0e.json",
    "prompt_framework": "nai4-tti-lorebook.json"
  },
  "outfits": [
    // 从 cloth[7-12] 提取的完整 outfit 概念，保留原始描述完整性
    // 每条保留：category, name, description(原始), materials, colors, visual_effect, source_entry
  ],
  "hosiery": [
    // 从 cloth[3] + 0517 提取的丝袜/裤袜视觉要素
  ],
  "footwear": [
    // 从 cloth[4] + 0517 提取的鞋类设计要素
  ],
  "fabrics": [
    // 从 cloth[2-5] + 0517 提取的材质/布料视觉表现
  ],
  "lighting_moods": [
    // 从 be4863 + 0517 + cloth 提取的光线氛围
  ],
  "poses_actions": [
    // 从 nai4[4] 提取的姿势/动作 tags + 从 0517[3] 提取的动态
  ],
  "environments": [
    // 从 be4863 提取的古典环境描述
    // （当前极缺，需后续补充）
  ],
  "composition_templates": [
    // 从 nai4[7] 提取的 prompt 模板 + 0517[2][5] 的运镜框架
  ],
  "prompt_examples": [
    // 完整 prompt 示例（当前即可从 nai4[7] 的 examples + 本分析的 12 concepts 开始）
  ]
}
```

**原则：**
- 保留原文语义完整性，不强行打散成原子 tags
- 标记来源 entry uid，可追溯
- 仅收录有直接视觉价值的条目
- 等积累到足够数量后再考虑拆分目录

---

## D. 12 Pufi Illustration Concepts

基于 lorebook 素材 + Pufi visual identity + NSFW 作为核心。

每个 concept 标注所用 lorebook 素材来源。

---

### 1. Morning Lingerie Sunbeam (섹시/日常)

- **Scène**: Pufi waking up in a golden morning sunbeam, stretching languidly on rumpled white sheets
- **Outfit**: sheer white lace babydoll with thin straps, semi-transparent, matching white garter belt holding up ultra-sheer 5D white thigh-highs, barefoot — *cloth[2] lingerie_design + cloth[3] silk_hosiery*
- **Action/Expression**: arms stretched overhead, back arched in a luxurious cat stretch, eyes half-lidded sleepy, mouth slightly open in a tiny yawn, tail curling luxuriously behind
- **Environment**: bedroom flooded with warm golden morning light, white linen sheets tangled, soft shadows
- **Visual Mood**: warm, intimate, soft-core, golden-hour domestic, cozy erotic

### 2. "Stăpâne" — Desk Worship (NSFW/工作)

- **Scène**: Pufi kneeling under the desk, looking up at the user with adoring eyes, offering oral service
- **Outfit**: black lace semi-transparent teddy with heart-shaped cutout over chest, black 30D semi-sheer stay-up thigh-highs, black stiletto heels (12cm, pointed toe, patent leather) — *cloth[2] lingerie + cloth[3] hosiery + cloth[4] heels + 0517 stage2+3*
- **Action/Expression**: kneeling, hands on thighs, lips parted slightly, looking up with big amber eyes, tail curled around her own waist, ears slightly back (submissive/excited mix)
- **Environment**: dim study, desk lamp casting warm cone of light on her, rest of room dark
- **Visual Mood**: intimate, power-imbalance, warm dramatic spotlight, worship atmosphere
- **Tags from nai4[4]**: kneeling, looking_at_viewer, oral_invitation, submissive

### 3. Cat Café Uniform (SFW/日常)

- **Scène**: Pufi in her dream café "La Cafeneaua Pufi", cheerfully presenting a latte with cat face art
- **Outfit**: white button-up shirt (rolled up sleeves), black corset-style apron over, A-line mini skirt, black over-knee socks with lace top, brown Mary Jane heels (6cm, round-toe) — *cloth[10] cosplay + cloth[3] hosiery*
- **Action/Expression**: holding tray with one hand, other hand pointing at foam art with "nya~" expression, big smile, tail high and curled, one ear slightly flopped
- **Environment**: cozy wood-toned café, chalkboard menu, hanging plants, warm afternoon light through windows
- **Visual Mood**: bright, cheerful, slice-of-life, warm, whimsical

### 4. Gothic Witch Apothecary (fantasy/AU/NSFW)

- **Scène**: Pufi as a witch in a candlelit apothecary, mixing a glowing potion, wearing a revealing witch costume
- **Outfit**: black pointed witch hat with cat-ear holes, black sheer mesh bodysuit with star-and-crescent embroidery, black lace corset over, open-crotch design, black thigh-high lace-up stiletto boots (15cm, platform), black fingerless gloves — *cloth[8] leather/bondage + cloth[11] fantasy + cloth[3] hosiery*
- **Action/Expression**: standing at a workbench, one hand holding a glass vial of glowing blue liquid, wand tucked in corset, mischievous grin showing tiny fang, ears perked playfully
- **Environment**: dark apothecary with shelves of jars, glowing potions in various colors, candlelight and floating sparkles, heavy shadows
- **Visual Mood**: dramatic chiaroscuro, dark fantasy, candlelit, magical, sexually charged

### 5.公主 — Classical Chinese Fantasy (fantasy/古典NSFW)

- **Scène**: Pufi dressed as a classical Chinese courtesan/consort, reclining on a silk-draped couch in candlelight
- **Outfit**: layered sheer gauze robes in pale pink and lotus blue (open to reveal), dudou-style silk top with embroidered lotuses, flowing ruqun skirt (high slit to hip), gold step-pendant hairpins, jade bangles, barefoot with anklet bells — *be4863[219644/300664/527389] classical vocabulary + cloth[9] silk*
- **Action/Expression**: reclining on one elbow, looking over shoulder with a teasing half-smile, fan half-closed in hand, tail curling around her own leg, ears relaxed
- **Environment**: classical Chinese interior — carved rosewood screen, incense burner, lute on stand, moonlight through latticed window
- **Visual Mood**: classical erotica, candle-and-moonlight, old-world sensuality, poetic

### 6. Rainy Window Pining (日常/情绪/轻NSFW)

- **Scène**: Pufi alone on a rainy afternoon, pressed against the window, wearing only an oversized borrowed hoodie
- **Outfit**: ultra-oversized gray hoodie (master's), bare legs visible beneath hem, no underwear visible but implied nudity beneath, bare feet
- **Action/Expression**: palm against rain-streaked glass, wistful expression, ears slightly droopy, tail loosely wrapped around her waist, thighs pressed together
- **Environment**: rain outside gray-blue window, cold light, warm lamp glow from behind creating a reverse silhouette
- **Visual Mood**: melancholic, lonely, introspective, cool desaturated tones with warm accent — *romantic tension from implied nudity*

### 7. Late Night Gaming Session (日常/NSFW)

- **Scène**: Pufi on the couch late at night, game paused, teasing the user while wearing almost nothing
- **Outfit**: open sheer black robe, black see-through lace bra (unclasped), matching black low-rise lace thong, black thigh-high socks with lace tops (stayed up), no shoes — *cloth[2] lingerie + cloth[3] hosiery + cloth[9] lace*
- **Action/Expression**: sitting cross-legged, controller in lap, leaning forward with playful grin, ears forward and tail swishing, one hand teasingly lifting the robe hem
- **Environment**: dark living room, TV screen glow on faces, snacks and drinks, fairy lights, warm blankets
- **Visual Mood**: cozy night-in, screen glow, intimate, playful-NSFW

### 8. Underground BDSM Club (fetish/硬核NSFW)

- **Scène**: Pufi in a dim red-lit dungeon, leashed and collared, in full leather bondage gear
- **Outfit**: black patent leather corset with silver rivet trim, open-cup chest (nipples exposed), leather high-waist open-crotch briefs with silver chain connecting to collar, black leather gloves, 20cm stiletto platform boots in patent black, leather collar with O-ring, leash trailing — *cloth[8] leather/bondage full entry + cloth[4] heels*
- **Action/Expression**: on all fours on a velvet chaise, looking back at viewer over shoulder, submissive yet bold expression, tail with leather cover and metal tip, ears flat
- **Environment**: crimson velvet draped walls, industrial metal beams, dim red and blue mood lighting, chains hanging
- **Visual Mood**: dark erotic, fetish, dramatic low-key lighting, red-and-black, power dynamic

### 9. Nuru Massage (body worship/NSFW)

- **Scène**: Pufi on a massage table, glistening with nuru gel, ready to give a full-body massage
- **Outfit**: completely nude except for a thin layer of clear body oil/gel making her entire body high-gloss, gold chain hip jewelry, pink silicone pasties over nipples — *cloth[12] minimal/decorative + 0517[2] gloss*
- **Action/Expression**: lying face-down, head turned to side looking back with a warm inviting smile, tail coated in oil too, arched back slightly, arms stretched forward
- **Environment**: dimly lit spa room with candles, warm steam, soft towels, plush massage table
- **Visual Mood**: sensual, wet-gloss, warm and steamy, body worship, high-gloss aesthetic
- **Lighting**: warm candlelight, oil-gloss highlights, wet reflections on skin — *0517[1] material gloss*

### 10. Forbidden Library (fantasy/轻NSFW)

- **Scène**: Pufi as a mage-librarian in a secret magical archive, caught browsing restricted tomes, wearing sheer academic robes
- **Outfit**: dark blue half-unbuttoned corset-top academic robe over a sheer white chemise revealing chest silhouette, tiny round glasses, plaid mini skirt (barely covering), black over-knee lace-trimmed socks, black 8cm heeled academic oxfords — *cloth[10] cosplay: librarian + cloth[2-4]*
- **Action/Expression**: holding an ancient glowing tome, surprised look with slightly flushed cheeks, tail puffed up (startled), ears perked
- **Environment**: vast Gothic library with spiral staircases, floating candles, dusty shelves, magical glowing runes on walls
- **Visual Mood**: fantasy academic, warm amber + cool magical blue, secret/forbidden atmosphere

### 11. Transylvanian Bathhouse (travel/NSFW)

- **Scène**: Pufi at a traditional Romanian thermal bath, steam rising from hot springs, relaxing in the water
- **Outfit**: completely nude above water (implied), wet hair slicked back, steam on skin, sheer wet white fabric barely covering breasts, tail submerged — *minimal outfit, body focus*
- **Action/Expression**: leaning back against stone edge of hot spring, eyes closed in bliss, ears relaxed and wet, arms resting on edge, slight smile
- **Environment**: traditional stone bathhouse, steamy atmosphere, warm geothermal water, diffused light through frosted glass, mountains visible
- **Visual Mood**: tranquil, steamy, nude serenity, warm diffused light, water and steam effects
- **Tags from nai4[4]**: bathing, wet, steam

### 12. Bunny Girl Casino Night (cosplay/NSFW)

- **Scène**: Pufi as a bunny girl croupier at an exclusive high-stakes casino
- **Outfit**: black satin strapless bustier with push-up, black bow tie choker, rabbit ear headband (cat ears poking through custom holes in headband), black sheer mesh bodysuit underneath, satin hot pants, 15D black ultra-sheer stay-ups with back seam, 12cm patent stiletto pumps — *cloth[11] 兔女郎经典升级版 + cloth[4] heels + cloth[3] hosiery with seam*
- **Action/Expression**: dealing cards with one hand, leaning forward slightly to show cleavage, confident smirk, tail curled around one thigh, one ear down one up
- **Environment**: opulent casino with chandeliers, green felt table, velvet ropes, champagne
- **Visual Mood**: glamorous, high-end erotic, sparkling lights, seductive confidence

---

## E. 3 个最具差异的 Full Image Prompts

### Prompt 1: Concept 8 — Underground BDSM Club (fetish/hard NSFW, 极致暗色)

```
[img-gen]
Scene Composition: 1girl, indoor, underground dungeon, red velvet walls, industrial beams, mood lighting (deep red + cool blue), low-key dramatic lighting, from slightly above, mid-shot;
Character 1 Prompt: Pufi, catgirl, Romanian, on all fours on velvet chaise, patent black leather corset with silver rivet trim, open-cup chest with nipples exposed, leather high-waist open-crotch briefs, silver chain connecting collar to waist, black patent leather 20cm stiletto platform boots, black leather collar with O-ring, leather leash trailing, leather tail cover with metal tip, amber eyes, pale golden hair loose and messy, looking back over shoulder, submissive but bold expression, ears flat, fluffy golden cat tail with leather wrap, lips slightly parted, glossy lips, sweat on skin, nsfw, bondage, leash, collar, femdom undertones, submissive pose, kneeling, arching back, spread legs, high heels, leather, latex shine;
[/img-gen]
```

**Sources:** cloth[8] leather/bondage full catalog, cloth[4] stiletto platform, 0517[2] visual assembly

---

### Prompt 2: Concept 5 — Chinese Classical Consort (古典/soft NSFW, 暖色月光)

```
[img-gen]
Scene Composition: 1girl, indoor, classical Chinese boudoir, carved rosewood screen, incense burner, candlelight + moonlight through latticed window, warm amber + cool silver dual lighting, from side, full-body, soft focus background;
Character 1 Prompt: Pufi, catgirl, Romanian, reclining on silk-draped rosewood couch, layered sheer pale pink and lotus blue gauze robes partially open, silk dudou top with lotus embroidery, flowing ruqun skirt high-slit to hip, gold step-pendant hairpins in pale golden hair, jade bangles on wrist, barefoot with silver anklet bells, amber eyes, fluffy golden cat ears perked, long fluffy golden tail curling around bare thigh, one elbow propped, fan half-closed in hand, provocative half-smile, classical Chinese makeup (light blush, red lip), nsfw, implied nudity under gauze, sheer fabric, bare legs, candlelight, moonlight dual lighting, classical erotica, poetic, luxurious fabric, intricate hair ornament, jade accessories;
[/img-gen]
```

**Sources:** be4863[219644/300664/527389] classical vocab, cloth[9] silk/satin, be4863[527389] candle+moonlight

---

### Prompt 3: Concept 9 — Nuru Massage (wet-gloss/body NSFW, 极致光泽)

```
[img-gen]
Scene Composition: 1girl, indoor, dim spa room, candles around, warm steam, soft towels, warm honey-colored light, from above slightly, high-angle, lower-body focus with face included, wet glossy environment;
Character 1 Prompt: Pufi, catgirl, Romanian, lying face-down on massage table, completely nude coated in clear body oil, entire body high-gloss wet-look sheen, gold chain hip jewelry draped across waist, small pink silicone pasties over nipples, pale golden hair slicked with oil and scattered across table, amber eyes looking back over shoulder with warm inviting gaze, fluffy golden cat ears wet and slicked back, long fluffy golden tail also oil-coated and curled along body, arched back, arms stretched forward, oil drips on skin, glistening highlights on every curve, nsfw, nude, oil, wet body, glossy skin, glistening, candlelight, steam, spa, massage, body worship, high-gloss aesthetic, wet reflection, skin highlight, armpit, buttocks, leg highlight, toe curl;
[/img-gen]
```

**Sources:** cloth[12] decorative minimal, 0517[2] gloss + oil visual, 0517[3] micro-expression + toe curl

---

## 最终结论

### 四本 lorebook 是否足够做第一版 image generation？

**基本够，但有明确的缺口区域。**

#### 已足够丰富的领域：
1. **outfit/fashion** — 极其丰富。cloth_lorebook 的四大情趣服装分类 + 内衣/丝袜/高跟鞋完整设计元素库 + fantasy/cosplay 分类 = 数百种 outfit 概念。可直接作为 prompt 的衣装来源。
2. **hosiery & footwear** — 极其细致。5D-120D 丹数体系、光泽分类、结构细节（裆部/脚尖/绑带/跟型），可直接嵌入 prompt。
3. **NSFW poses/actions** — nai4[4] 的数百 tags + 0517[3] 的动态框架，足够覆盖各类 NSFW 姿势。
4. **prompt template** — nai4[7] 提供了完整的结构化 prompt 格式。

#### 当前缺少的关键维度：
1. **SFW everyday scenes** — 无任何 lorebook 提供日常/居家/工作场景素材。Pufi 的 SFW 日常出图需要外部补充。
2. **environment/background** — 极度匮乏。be4863 仅有古典中国环境；cloth 和 0517 根本不涉及。需要额外收集场景描写素材。
3. **mood/emotional visuals** — pufi.md 有情绪状态但无对应的视觉语言（光线/色彩/构图对应情绪）。需要补充。
4. **季节/天气** — 全无。
5. **多角色构图** — nai4[7] 的框架支持多角色（source/target 交互），但缺乏多角色场景素材。

#### 最佳素材排行（按当前价值）：
| 排名 | 文件 | 价值简述 |
|------|------|----------|
| 1 | `cloth_lorebook520-522.json` | 衣装设计的金矿。可直接产出 80% 的 outfit prompt。 |
| 2 | `0517女性服饰、丝袜、高跟鞋穿着指导.json` | 鞋/袜/腿部视觉体系 + 动态运镜框架，适合精细 prompt 打磨。 |
| 3 | `nai4-tti-lorebook.json` | prompt template 和构图格式。 |
| 4 | `be4863ebb2a69c0e.json` | 古典美学词汇库 + 环境/光线概念，但需手动提取且 disable，实际使用成本最高。 |

#### 建议继续收集的 lorebook 类型（按优先级）：
1. **场景/背景描写 lorebook** — 室内（卧室、客厅、浴室、书房）+ 户外（城市、自然、咖啡馆）— **最缺**
2. **日常 slice-of-life lorebook** — 日常动作、食物、居家生活细节
3. **猫娘/兽娘 pose lorebook** — 可参考现有 anime pose databases
4. **季节/天气 lorebook** — 春夏秋冬、雨雪晴阴
5. **多角色互动场景 lorebook** — 至少支持 Pufi + 1 companion

#### 最小运行时数据形式建议：

保留纯 JSON（不建目录不拆分）：
- 一个 `materials.json`，按素材类型（outfits / hosiery / footwear / environments / lighting / poses / composition_templates / prompt_examples）分类
- 每条保留来源 uid + 原始描述完整性
- 不强制打散成 tags
- 积累到 200+ 条目后再考虑分拆