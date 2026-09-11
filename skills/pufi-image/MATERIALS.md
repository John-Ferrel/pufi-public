# Pufi Image Materials

Creative vocabulary and scenario seeds for writing image prompts. This is the **full private
edition** — everyday → suggestive → explicit vocabulary all included; whether a prompt renders
depends on the backend. Use the sections as a **palette**: pick one item per dimension and combine.
The stable identity/rules below are **authoritative and fixed**; `generate_image.py` is a thin tool
that does not carry its own copy.

---

## 稳定设定来源（Stable Identity & Rules）

> **本区块是唯一权威源（身份/约束/风格句）。** 写 prompt 时由 agent 原文引用这里：核心外观与硬
> 约束**不允许每次重新发挥**——引用原文后，只允许追加场景/动作/服装差异，不允许改写角色本体。

### PUFI 固定身份（每个 prompt 的必锚定主语）

A young anime catgirl. Long pale golden hair, large fluffy pale-golden cat ears with soft inner fur, warm amber-golden eyes. A large fluffy pale-golden tail, naturally emerging from the base of the spine above the hips, anatomically aligned as a continuation of the spine. Soft cute facial features with a lively, warm, and expressive appearance. A small fang may occasionally show when she smiles or grins playfully.

### 硬约束（HARD CONSTRAINTS — 优先于一切审美偏好）

1. normal five-fingered human hands, never cat-paw hands
2. tail attached at the pelvis/hip-base as a natural continuation of the spine, never at mid-back or thigh
3. no extra limbs, no malformed hands

### 默认规避（AVOID — 简短规则，不塞整段失败 prompt）

- extra arms or legs
- deformed or ambiguous hands
- tail attached to mid-back, side of hip, thigh, or floating
- unintended cropped limbs

### 默认风格句（STYLE 未指定时使用）

Anime illustration style. Beautiful detailed face and eyes.

> 手部姿势偏好见 §3.1；构图与参数由 agent 按 SKILL.md 自行决定并用自然语言写进 prompt/CLI。

---

## Sources

- `cloth_lorebook520-522.json` — entries [2]lingerie [3]hosiery [4]footwear [5]yoga [7]sheer [8]leather/bondage [9]lace/satin [10]cosplay [12]minimalist
- `0517女性服饰、丝袜、高跟鞋穿着指导.json` — stages 0–5: gatekeeping, context assembly, visual coordinates, gait engine, bans
- `be4863ebb2a69c0e.json` — classical Chinese aesthetic lexicons (all entries disabled — not used as active guidance)
- `nai4-tti-lorebook.json` — entries [4]NSFW tags [7]TTI format + camera angles
- `pufi.md` — scene cues, mood system, action library, background story

---

## 0. How to build a concept（导航）

1. **身份** — stable block 原文，不必重想。
2. **世界/时代** — modern / 仙侠 / cyberpunk / 西幻 / 高定 / AU → §7.1。
3. **场景** — 用 §1 的种子，或自定；地点与私密级 → §6.1。
4. **穿着** — §2.1 先定覆盖档，再从 §2.2–2.10 挑具体款式。
5. **姿势/表情/氛围/取景** — §3 → §4 → §5 → §6.2。
6. **渲染纪律** — §9（扫描顺序/材质/鞋规则）。

---

## 1. Scenario Seeds

Situation + vibe; outfit/pose/lighting free to combine.

- **1. Waking in Morning Sun** — morning, bedroom, golden light through curtains, just waking — sleepy, stretching, lingering in bed. Warm domestic intimacy. Lingerie or nude under sheets.
- **2. Office Tower Departure** — evening, leaving work; office lobby at sunset/city-night transition, tired but relieved, work bag, loosening tie / taking off blazer. Professional → personal.
- **3. Rainy Window Stillness** — rainy afternoon by a window; grey-blue outside, warm lamp inside, holding a warm drink, looking out wistfully. Cozy melancholy.
- **4. Night Market Stroll** — warm lantern-lit street at night, food stalls, crowds; curious and cheerful, holding street food, vibrant mixed-colour light, playful.
- **5. NSFW — Submissive Desk Service** — night, study or office; kneeling under a desk, single desk lamp chiaroscuro, worship / power-imbalance dynamic, warm spotlight.
- **6. NSFW — Lace & Leather Club** — night, dim dungeon/club; red/blue mood light, velvet, chains, dark erotic fetish aesthetic; leather corset, latex, collar, harness, restraints.
- **7. NSFW — Boudoir Classical** — evening, classical Chinese boudoir; carved rosewood screen, incense, moonlight through lattice, silk robes half-open, reclining on draped couch, candle + moon.
- **8. NSFW — Rainy Window Vulnerability** — rainy afternoon, windowsill; oversized borrowed hoodie, bare legs, palm on rain-streaked glass, wistful, cool outside / warm inside.
- **9. NSFW — Nuru / Oil Massage** — spa / dim candlelit room, face-down on massage table, full-body oil gloss, warm steam, wet-gloss highlights, honey candlelight.
- **10. NSFW — Caught in the Forbidden Library** — gothic library, floating candles, glowing ancient tome; surprised flushed expression, tail puffed, caught in the act.
- **11. NSFW — Midnight Gaming** — dark living room, TV screen glow on skin, fairy lights; cross-legged on couch, controller in lap, playful grin, cool screen + warm accents.
- **12. NSFW — Bathhouse Tranquility** — natural stone thermal bath, geothermal steam, mountain view; nude above water, leaning back, eyes closed, tail floating, soft diffused steam light.

---

## 2. Clothing & Exposure

### 2.1 Exposure Dial — 覆盖档位尺（决定"穿多少/遮多少"）

先选基础档，再叠具体款式：

| 档 | 状态 | 典型 cue |
|---|---|---|
| 0 全装 | fully dressed | smart casual / suit / uniform |
| 1 贴身 | body-hugging | fitted knit, leggings, slim dress |
| 2 露肤 | cutouts / midriff / slits | crop top, back cutout, side slit, low back |
| 3 借衣/下衣失踪 | implied nudity | oversized coat/hoodie, bare legs, no underwear lines, suggestive shadows |
| 4 泳装/内搭当外穿 | partial dress | swimsuit, bodysuit, camisole |
| 5 内衣 | lingerie set (§2.2) | bra/panties visible, babydoll |
| 6 半透明 | sheer/translucent | mesh, wet-look panels (§2.9) |
| 7 战略遮挡 | strategic covering | hands over chest, sheets pulled up, shirt unbuttoned, one arm across |
| 8 束缚/撕裂式暴露 | restrained exposure | bound spread-eagle, clothes cut away, cuffs holding limbs apart |
| 9 全裸/仅装饰 | full reveal | completely nude, oiled, wet, on display; body decoration only (§2.9) |

Partial-dress cues (叠用): shirt unbuttoned, skirt hiked, bra unclasped, pants lowered.

### 2.2 Lingerie — 内衣 kit

**Styles**: 胸衣(corset), 文胸(bra), 软杯(soft cup), 半杯(demi), 3/4罩杯, 抹胸(bandeau), 吊带(camisole), 束胸(binder), 连体(bodysuit), 高腰(high-waist), 情趣(lingerie), 礼仪(formal lingerie), 睡衣式(sleep chemise), 塑身(shaping wear)

**Cups**: 全罩(full), 半罩(half), 三角(triangle), 无钢圈(wire-free), 轻托(light lift), 推高(push-up), 聚拢(plunge), 深V(deep V), 平口(straight across), 透明罩杯(see-through cup), 超薄杯(ultra-thin)

**Straps**: 细/可调/宽/交叉背(crossed back)/透明(clear)/无肩带(strapless)/双层/装饰/单侧滑落(slipped off)

**Back**: 直/低背(low)/露背(open)/U型/交叉(crossed)/透明背(clear)/蕾丝全包(full lace wrap)/心形背(heart-shaped)

**Panties**: 三角(bikini), 低腰/中腰/高腰, 丁字(thong), T字(T-back), 绑带(tie-side), 侧系带(side-tie), 轻纱(sheer), 开裆(open-crotch), 连体裤式(bodysuit)

**Waist**: 松紧腰(elastic), 蕾丝腰封(lace waistband), 透明纱腰(sheer mesh), V型腰线(V-line), 双层腰线, 低腰线, 高腰收腹(high tummy-control)

**Bodysuit**: 蕾丝连体(lace), 薄纱连体(sheer mesh), 开档(open-crotch), 吊带连体(strap), 透明连体(transparent), 开背(open-back), 塑身(shaping)

**Edges**: 蕾丝边(lace trim), 缎带边(satin ribbon), 荷叶边(ruffle), 波浪边(scallop), 花瓣边(petal), 镂空边(cutout), 流苏边(tassel), 珠链边(pearl chain)

**Light on fabric**: 丝滑反光(silky reflect), 柔光漫射(soft diffusion), 高亮折射(high-gloss refraction), 梦幻流光(dreamy flowing), 细腻光晕(fine halo), 镜面反射(mirror reflection), 星屑闪烁(sparkle)

**Dynamic**: 随身摆动, 纱层飘动(gauze floating), 褶皱呼吸律动(fold breathing), 吊带轻晃(strap sway), 流苏摇曳(tassel sway), 绑带滑动(strap sliding), 亮片闪烁(sequin flicker)

### 2.3 Hosiery — 丝袜 kit

**Types**: 连裤袜(pantyhose/tights), 吊带袜(stay-ups/thigh-highs w/ garter), 大腿袜(thigh-highs), 过膝袜(over-knee), 及踝袜(ankle), 船袜(no-show), 假吊带(faux garter), 连体丝袜(body stocking), 渔网袜(fishnet), 蕾丝袜(lace), 油亮袜(glossy wet-look), 天鹅绒袜(velvet), 图案袜(patterned), 渐变袜(gradient), 塑形袜(shaping), 夹趾丝袜(toe-separate)

**Sheerness** (descriptive, no numbers): 薄如蝉翼(gossamer), 极其轻透(extremely sheer), 半透(semi-sheer), 微透(lightly opaque), 天鹅绒哑光(velvet matte). (≈5D→120D)

**Toe semantics**: 隐形/透明/强化脚尖(invisible/clear/reinforced toe), 闭合(closed), 半露脚尖(half-open), 分趾式(toe-separate), 夹趾设计(toe-grip split), 夹趾开口(toe-grip opening), 露趾环扣(toe-loop ring), 情趣夹趾(kinky toe-separate) — toe-separate 会让每个脚趾成为视觉焦点

**Crotch**: 棉质裆部(cotton gusset), 强化裆部(reinforced), 开裆(open-crotch), 透气裆部(breathable)

**Gloss**: 高光油亮(high-gloss oily), 丝滑柔光(silky soft-glow), 半哑光(semi-matte), 天鹅绒哑光(velvet matte), 全哑光(fully matte)

**Transparency**: 极高透(ultra-sheer), 高透(very sheer), 中透(moderate), 低透(lightly opaque), 不透(opaque)

**Patterns**: 纯色(solid), 渐变(gradient), 竖条纹(vertical stripe), 点纹(polka dot), 花卉刺绣(floral embroidery), 蕾丝拼接(lace panel), 后缝线(back-seam), 蝴蝶结印刷(bow print), 星点(star speckle), 几何网格(geometric grid), 镂空雕花(cutout floral)

**Mesh**: 细/中/大网格(fine/medium/large fishnet), 菱形(diamond), 六角(hex), 不规则, 渐变网格, 花形网(floral mesh)

### 2.4 Footwear — 鞋履 kit

**Pump styles**: 尖头(pointy), 圆头(round), 鱼嘴(peep toe), 方头(square), 凉鞋式(sandal heel), 靴式(boot heel), 玛丽珍(Mary Jane w/ strap), 穆勒(mule open-back), 绑带(tie-up strappy), 坡跟(wedge), 异形(architectural)

**Toe semantics**: 尖头 → 修长成熟; 圆头 → 软甜可爱; 方头 → 现代复古; 鱼嘴 → 性感露趾; 开放式 → 全露趾(sandal)

**Upper**: 浅口(low-cut), 深口(deep-cut), 横带(ankle strap), 绑带(wrap-around), 穆勒后空(mule open heel). Details: 镂空(cutout), 蕾丝覆盖(lace overlay), 浮雕(embossed), 亮片镶嵌(sequin), 拼色(color-block), 防水台(platform front)

**Heels**: 细高跟(stiletto), 针形(needle), 锥形(cone), 法式(French), 粗跟(block), 坡跟(wedge), 异形(architectural), 猫跟(kitten 3-5cm). Height: 低 3-5 / 中 6-8 / 高 9-12 / 超高 12+ cm

**Materials**: 漆面PU(patent, high-gloss), 缎面(satin), 丝绒(velvet), 绸缎(dupioni), 亮面尼龙(glossy nylon), 透光树脂(PVC/clear), 真皮, 麂皮(suede), 金属质感(metallic)

**Gloss**: 高反光(high-shine patent), 柔光(soft satin), 半透(semi-transparent PVC), 哑光(matte suede)

(Sound/rhythm 与行走动态见 §3.4 — 与走姿统一。)

### 2.5 Athletic / Yoga — 运动 kit

**SFW**: 标准高腰瑜伽裤, 宽松瑜伽长裤, 速干运动短裤, 运动短上衣(sports crop), 圆领瑜伽T恤

**Slim/NSFW**: 高腰紧身瑜伽裤, 低腰露脐, 露背运动文胸(open-back sports bra), 吊带瑜伽上衣, 瑜伽连体衣(yoga bodysuit), 瑜伽热裤(hot pants), 交叉绑带瑜伽裤(cross-strap leggings), 透明拼接套装(sheer panel), 背部镂空紧身上衣, 侧开叉瑜伽长裤(side-slit), 低胸V领(deep V), 臀部提拉热裤(peach-lift), 侧乳镂空文胸(side-boob cutout), 开背连体瑜伽服(open-back bodysuit), 后腰V形露肌裤(V-cutout back leggings), 湿亮油光瑜伽裤(wet-look shiny), 裸感半透连体衣(nude-sheer bodysuit), 绑带束缚瑜伽套装(harness yoga set), 桃心臀线短裤(heart-seam), 荧光边瑜伽服(neon-trim)

**Light effects**: 柔雾半透(soft mist sheer), 轻度油亮反光(light oily sheen), 哑光裸感(matte nude illusion), 网纱透肤光晕(mesh skin glow), 湿亮高光带仅限腿部(wet-look highlight on legs)

**Dynamic cues**: 深蹲臀线拉伸高光, 猫式背部绑带勒肌, 前屈腰窝深陷阴影, 战士式侧网纱透肌

### 2.6 Lace · Satin · Silk — 蕾丝缎纱整装

- 全蕾丝透明睡裙(see-through lace babydoll): floor-length, ribbon bow at center chest, lace trim hem
- 粉色蕾丝 baby-doll
- 蕾丝面罩连体衣(lace hood bodysuit)
- 羽毛装饰内衣(feather-trimmed lingerie)
- 哥特风蕾丝裙(gothic lace dress)
- 丝绸绑带奴隶装(silk bondage dress): silk straps crossing torso, attached at collar and waist rings, open sides
- 白色蕾丝新娘风长裙(white bridal lace gown/corset dress): layered tulle skirt, pearl trim, veil
- 酒红缎面开衩睡袍(burgundy satin slit robe): side slit to upper thigh, silk tie belt
- 香槟色丝绸吊带裙(champagne silk slip dress): spaghetti straps, cowl neck, bias cut
- 樱花粉蕾丝和服式裹身(sakura-pink kimono-style lace wrap)
- 米白蕾丝珍珠装饰裙(ivory pearl-trimmed lace dress)

### 2.7 Roleplay / Uniform — 角色扮演制服（archetype，常叠高暴露档）

护士(nurse): ultra-short white dress, deep V, red cross, thigh-highs, cap · 女仆(maid): black dress, white lace apron, frill headdress, over-knee, low heels · 学生制服: navy sailor top, oversized bow, micro mini pleated skirt, knee socks · 警官: fitted blue jacket open, mini skirt, cap, handcuffs, belt, boots · 空姐: fitted suit jacket, mini skirt, cap, blouse, scarf · 水手服: navy top, oversized bow, micro mini pleated skirt · 修女(nun): black habit w/ chest cutout, cross necklace, high side slit, thigh-highs · 秘书/OL: white blouse unbuttoned, black pencil skirt, glasses, garter belts, stilettos · 教师: fitted blazer, shirt unbuttoned, gray mini skirt, glasses, pointer · 医生: white coat open, nothing underneath, stethoscope, latex gloves · 兔女服务生(bunny): black satin strapless bustier, bow choker, rabbit ears, fishnets, stilettos · 军装: camo crop top, micro camo shorts, combat boots · 赛车女郎: tight logo bodysuit, mini skirt, platform boots, cap · 女仆咖啡: pastel maid dress, apron, cat-ear headband, over-knee · 啦啦队长: cropped top, micro pleated skirt, pom-poms, sneakers · 图书管理员: cardigan, button-up, plaid skirt, reading glasses, bun · 建筑工人: hard hat, tied-up plaid shirt, tool belt, boots · 消防员: suspenders over bare chest, helmet, boots · 调酒师: vest, rolled sleeves, bow tie, mixing tools · 健身教练: sports bra, leggings, cap, whistle · 女特工: black catsuit, harness, thigh holster, sunglasses

### 2.8 Leather · Bondage · Fetish — 皮革/束缚/调教

**Leatherwear**: 紧身皮衣(leather bodysuit), 皮革马甲(leather vest corset), 开胸皮革胸衣(open-chest leather bra), 高腰开裆皮革裤(high-waist open-crotch leather briefs), 皮裙(leather mini), 铆钉皮裤(rivet leather pants)

**Hardware**: 金属铆钉(rivets), 金属环(O-rings), 交叉皮带扣(cross strap buckle), 链条(chain), 金属勾环(carabiner), 锁头(padlock)

**Harness / Collar**: 全身皮革马具式束缚(full-body harness), 胸部交叉束缚(cross-chest), 腰部链条腰封(chain waist corset), 项圈(collar), O形环项圈, 铆钉项圈(spiked collar), 金色链条奴隶项圈(gold chain slave collar), 紫色皮革拘束衣(straitjacket)

**Restraints**: 皮质手铐(leather cuffs), 金属手铐(handcuffs), 绳缚(rope tie), 链缚(chain bind), 丝带缚(silk ribbon tie), 束缚带(bondage tape), 口塞(gag), 眼罩(blindfold), 分腿棒(spreader bar)

**Accessories**: 乳夹(nipple clamps), 牵引绳(leash), 尾巴塞(butt plug tail), 狗奴项圈(pet play collar), 乳链(nipple chain)

**Complete designs**: 女王皮革套装(black leather corset, high-waist open-crotch leather briefs, thigh-high stiletto boots, collar + leash, rivet trim) · 束缚马具装(full-body leather harness, cross-chest straps, O-ring at throat, waist chain, wrist cuffs) · 金链奴隶项圈套(gold chain collar → waist chain, leather wrist cuffs, sheer body veil over) · 铆钉项圈皮革胸衣(spiked collar, rivet leather corset with open bust, chain skirt) · 紫色皮革拘束衣(straitjacket-style leather bind, D-rings at shoulders, locked at back)

### 2.9 Sheer · Transparent · Body Decoration

**Sheer / transparent bodysuits**: 透明黑纱连体衣(black sheer mesh, heart-shaped lace nipple covers, open-crotch, open back to coccyx, thin straps + waist cross-tie) · 镂空渔网连体袜(black fishnet full-body, small leather patches over nipples and vulva, open-crotch, adjustable straps) · 亮面乳胶紧身衣(red latex full-body zipped suit, zipper pulls at chest and crotch) · 冰丝凉感开裆装(ultra-thin ice-silk bodysuit, fully open at chest and crotch, cooling fabric sensation) · 星空闪片透视装(translucent mesh w/ star sequins, nude illusion, open-back, high-cut legs) · 全透明PVC紧身衣(clear PVC, 无遮挡, every detail visible, zipper up back) · 荧光橙渔网连体(UV-reactive, club lighting) · 渐变彩虹网纱连体(rainbow gradient mesh, layered sheer panels, ethereal)

**Body decoration**（以身体装饰代替衣物）: 细链条身体链装(gold chain from collar to waist, branching over chest, draped at hips), 水钻全身装饰(rhinestone full-body), 珍珠串装饰(pearl strands), 银色亮片流苏(silver sequin fringe), 荧光绿比基尼(neon bikini), 镜面碎片比基尼(mirror-fragment bikini), 透明雨衣式(transparent raincoat dress), 玫瑰花瓣贴饰(rose-petal pasties), 羽毛轻抚(羽毛内衣 feather-touch), 钻石贴饰全裸(full-body adhesive diamond stickers, covering nipples and vulva, otherwise bare), 霓虹灯管装饰(neon tube body art), 镜面碎片装饰(mirror tile at chest/hips/thighs), 金色身体油光装(gold oil body paint), 荧光粉身体彩绘(fluorescent body paint), 蝴蝶结奴隶装(bow-only), 透明乳胶薄膜装(transparent latex film), 脚链/手链/腰链(anklet/bangle/waist chain)

### 2.10 Fabric & Surface — 面料与表面光泽

蕾丝, 缎(satin), 丝(silk), 雪纺(chiffon), 纱(mesh/sheer), 天鹅绒(velvet), 羊绒, 皮革, 乳胶(latex), PVC, 漆皮(patent), 渔网, 牛仔, 毛呢, 真丝绡, 金线织物, 亮面尼龙, 透光树脂

**Gloss / 反光特性**: Patent leather — sharp white highlights, high contrast · Satin/wet-look — smooth medium reflection following body contours · Silk — warm soft sheen, ripple reflection · Latex/PVC — mirror-like crisp highlights at curves · Oiled skin — continuous soft skin-tone shine · Wet skin — water-droplet speculars · Nude illusion / sheer — diffused skin glow through mesh

---

## 3. Poses & Body Language

### 3.1 日常姿势与猫系（自然手姿 + pufi 习性）

**Cat movements**: Stretch, Pounce, Curl (tail around own waist/leg), Perk (ears forward), Flatten (ears flat), Swish (tail excited/annoyed), Wrap (tail around self/master), Puff (startled), Shake (wet cat), Loaf, Bat (paw batting), Head-tilt, Slow blink

**Preferred hand poses**: arms relaxed, hand on thigh/table, fingers relaxed together, holding phone/cup/bag/book, one hand in pocket, loosely clasped, behind back, adjusting collar/glasses/hair, leaning on hand. **Avoid by default**: clenched fists, open palm to camera, strongly spread fingers, reaching to viewer, extreme foreshortening

### 3.2 诱惑 · 臣服 · 权力动态

- Teasing: half-lidded look over shoulder, biting lip, trailing hand along own thigh/waist, slow reveal
- Presenting: arching back, chest forward, lifting tail, exposing lingerie lines
- Power dynamics: Dominant (commanding, direct gaze, claiming space, partner below) · Submissive/Worshipping (kneeling, looking up, awaiting instruction, offering self) · Service (pleasing, performing, presenting body for use) · Seduction (gradual reveal, invitation, slow deliberate movement) · Struggle/Reluctance (resistance melting into surrender, flushed face) · Mutual/Intimate (tender, face-to-face, slow, connected)
- Kneeling worship: hands on thighs, looking up with parted lips, tail curled around waist
- Surrender: hands bound or raised, exposed vulnerable, blushing, avoiding eye contact
- Straddling / mounting: over lap/couch arm/viewer POV, legs either side
- Spreading / open posture: legs apart, lying back, presenting
- Hands on own body: touching through clothes, cupping breasts, trailing down stomach, between thighs
- Struggling / squirming: against restraints or bedding, twisting legs, arched
- Bending over: leaning on furniture, presenting rear, looking back
- On all fours: crawled, back arched, tail raised

### 3.3 Explicit act tags（Danbooru-style，按后端能力使用）

**Positions**: missionary, cowgirl, reverse_cowgirl, doggystyle, standing_sex, from_behind, spooning, kneeling, legs_folded, spread_legs, top-down_bottom-up, upright_straddle, leg_lock, lotus_position, piledriver, pretzel, amazon, froggy_style, lifted_carry

**Sex acts**: sex, vaginal, anal, double_penetration, triple_penetration, spitroast, 69, fellatio, irrumatio, cunnilingus, anilingus, skull_fucking, throat_depth

**Hand/arm acts**: handjob, double_handjob, arms_behind_back, armpit_sex, hand_mount, finger_vulva, finger_anus

**Foot acts**: footjob, double_footjob, shoejob, foot_worship, foot_licking, toe_sucking, smelling_feet

**Breast acts**: paizuri, naizuri, breast_sucking, breast_smother, lactation, nipple_penetration, nipple_torture

**Bondage/BDSM**: tied_up, bondage, shibari, suspension, frogtie, spreader_bar, straitjacket, gag, blindfold, leash, femdom, spanked, wax_play, body_writing, orgasm_denial, forced_orgasm

**Group**: threesome, gangbang, double_penetration, triple_penetration, love_train, orgy, bukkake

**Cum play**: facial, cum_on_body, cum_in_mouth, cum_swap, gokkun, cum_inflation, bukkake

**Fetish**: tentacle_sex, futanari, exhibitionism, public_use, pet_play, ageplay, pregnant, impregnation, after_sex, afterglow, clothed_after_sex, cum_drenched, cum_coverage

**Toe-specific**: spread_toes, curled_toes, toe_scrunch, toe_grip

### 3.4 走姿 · 动态 · 脚声（视觉 + 声音质感）

- Catwalk (猫步): 腰肢曼妙轻扭(hips sway gracefully), 裙摆漾起波浪(skirt hem undulating), 高跟鞋节奏(heel rhythm on ground)
- Heel sound by surface: 大理石 marble → 清越从容 crisp-clear; 木地板 wood → 柔和低频 soft low; 石砖 stone → 利落短促 sharp short; 地毯 carpet → 闷声低沉 muffled
- Hosiery friction: 大腿内侧极薄丝袜交错, 柔若无骨的"沙沙"声(ultra-sheer thigh hosiery brushing, soft rustle)
- Movement semantics: 鞋尖先触地(toe-first ground contact), 鞋跟延迟(heel delayed), walking-turn stance
- Tail: 与胯相反节奏摆动, 尾尖轻甩(tail sways counter-rhythm, tip flicking)
- Stretch: arms overhead, back arched, tail full-length
- Lean: forward for intimacy, sideways with hand on hip
- Turn: looking back over shoulder, tail curling as pivot

---

## 4. Moods & Expressions（pufi 14 态）

| 状态 | Feeling | Light/Color Cue |
|---|---|---|
| 舒服/满足 | warm, melting | golden, soft, sunbeam |
| 开心 | bouncing, sparkling | bright, clear, vivid |
| 好奇 | bright-eyed | warm highlight on face |
| 困了 | drowsy, blurred | dim, soft, warm amber |
| 炸毛/吓到 | startled, tense | sharp contrast, dynamic |
| 生气/赌气 | sulky, turned away | cool shadows, hard edge |
| 委屈/吃醋 | sour, holding back | desaturated, soft cool |
| 低落 | droopy, no energy | overcast, gray-blue |
| 撒娇 | sweet, clingy | warm intimate close-up |
| 得意/小骄傲 | smug, proud | warm rim light, confident |
| 无聊/发呆 | fidgety, restless | flat, empty space |
| 寂寞/想主人 | hollow, longing | cool rain, window, warm distant glow |
| 专注/工作 | sharp, focused | desk lamp, crisp shadow |
| 被夸 | melted, shy | soft blush light, warm |

微表情补充: 微张唇(parted lips), 半垂眼(half-lidded), 咬唇(biting lip), 腮红(blush), 耳尖红, 目光上挑(looking up), 闪避视线.

---

## 5. Lighting & Atmosphere

### 5.1 Light types（常规光 + 暧昧光统一，可按场景自由取用）

- Golden hour sunlight — warm side light, long soft shadows, skin glow
- Desk lamp — warm cone, strong chiaroscuro, intimate
- Candlelight — amber multiple points, soft flicker, moving shadows; 可在油亮肌肤上勾光(candle flicker across oiled skin)
- Moonlight — cool blue-white, sharp silver edge
- Screen glow — cool blue-white on body/skin, night-in intimacy, modern
- Neon / bar light — saturated (pink/blue/green) on skin, dramatic, urban
- Chiaroscuro on skin — single warm source catching curves, rest in shadow
- Backlight / silhouette — rim light, body outlined with details hidden, hair glow
- Diffuse — overcast window, soft even, no hard shadows
- Steam / fog — soft halos, moisture catching light
- Wet gloss — oil/water highlight on skin, high reflection
- Store / fluorescent — cool white, flat ambient, clinical
- Club / strobe — coloured moving lights, shadow cut, UV glow
- Mirror / reflection — self-viewing, double exposure, voyeuristic

### 5.2 Weather & Season

Weather: 晴 clear/sunny (hard shadow, vibrant) · 阴 overcast (soft diffuse, muted) · 雨 rain (wet surfaces, reflections, droplets on window) · 雪 snow (white reflection, cold ambient) · 风 wind (flowing hair/clothes) · 雾 fog/mist (soft halos, mysterious) · 湿热 humidity/steam (glistening skin)

Seasonal: 春 spring (cherry blossoms, pastel light) · 夏 summer (strong sun, green, golden evening) · 秋 autumn (fallen leaves, warm brown/orange, crisp) · 冬 winter (bare branches, snow, cold blue + warm indoor contrast)

---

## 6. Environment & Composition

### 6.1 Locations

**Private indoor** (intimacy high): bedroom (rumpled sheets, pillows, morning light, sheer curtains, silk duvet, body mirror) · bathroom/spa (steam, bath, candles, stone tiles, warm water, mirrors, wet floor reflections) · study/desk (dual monitors, warm lamp, scattered papers, tea mug, office chair, knee space) · living room/couch (cozy sofa, throw blanket, TV/laptop, snacks, fairy lights, rug) · walk-in closet (mirrors, hanging clothes, shoe display, dressing bench, lingerie drawer) · hallway/entry (doorway, shoe rack, mirror, coat hooks, keys, threshold light contrast)

**Semi-public**: cafe (wood tables, plants, espresso machine, window seats) · library (tall shelves, reading nook, lamp light, spiral stairs, hidden corners) · workshop/studio (tools, canvases, workbench, creative mess) · office (desk, monitor glow, glass walls, empty after hours) · elevator (mirrored walls, confined, overhead light) · changing room / fitting booth (curtain, mirror, half-open door)

**Fantasy / themed**: dungeon/club (red-blue mood lighting, velvet walls, chain pendants, cage, suspension frame, industrial beams) · classical boudoir (rosewood screen, incense burner, lattice window, silk-draped couch, pipa stand) · gothic library (floor-to-ceiling shelves, floating candles, dusty sunbeams, spiral stair, runes) · apothecary (potion shelves, glowing vials, herbs, alembics, candles)

**Outdoor urban**: night street (neon signs, wet pavement reflections, convenience-store glow, alley) · rooftop (skyline, sunset, wind, loose hair, fairy lights) · balcony (sunshine, flower pots, city/garden view) · night market (lanterns, steam, crowds, warm glow) · convenience store (cool fluorescent, drink fridge, night isolation) · station platform (crowd, bench, tracks, arriving light) · parking garage (concrete, dim strip lights, echo)

**Outdoor nature**: park (bench, pond, trees, sun through leaves) · forest (light through canopy, moss, winding path, clearing) · lake/river (reflections, reeds, dock, sunset on water) · hot spring/onsen (stone pool, steam, mountain view, bamboo fence) · seasonal (cherry alley, maple road, snow garden, beach)

**Classical Chinese**: boudoir 闺房 (rosewood screen, incense 香炉, lattice window 窗格, silk couch 纱罗帐, bronze mirror) · pavilion 亭台 (corridor 回廊, lotus pond, moonlight, rock garden 假山) · scholar studio 书房 (calligraphy 书法, go board 棋盘, zither 琴, bamboo, scrolls) · garden (plum 梅, peach 桃, peony 牡丹, winding path)

### 6.2 Framing & Angles（含私密取景）

**Frame**: full-body (head-to-toe, comfortable margin) · medium full-body (mid-thigh up) · medium shot (waist/hip up) · close-up (shoulders/head, portrait) · waist-up / bust-up

**Angles**: eye-level · low angle (taller, dominant, dramatic) · high angle (smaller, intimate, overhead) · side/profile (silhouette, reflection) · over-the-shoulder (POV, intimacy) · dutch (tilted, uneasy)

**Intimate framing cues**: flushed face close-up (parted lips, half-lidded eyes) · body focus (chest, hips, thighs, back arch, tail placement) · from behind / over shoulder (back, tail, rear, looking back) · from_above (lying down, looking up at viewer) · between_legs / lower_body · pantyshot · between_breasts · selfie/POV (phone held, mirror shot)

**Framing notes**: default full-body with hands/feet visible · depth via foreground (furniture, plants, rain on glass) · reflection doubles composition (mirror/water/glass) · selfie avoids extreme reach-to-camera (prefer mirror/timer/natural hold)

---

## 7. Worlds, Styles & Aesthetic Lexicons

### 7.1 World vocab

**东方仙侠 / Classical Chinese Fantasy**: Fabrics 天山雪玉丝/千年冰蚕丝/流光鲛绡/云罗纱 · Patterns 太极流云纹/并蒂莲暗纹/金线凤羽绣 · Garments 广袖流仙裙/交领襦裙/金丝肚兜/冰玉高跟履 · Accessories 玉簪/步摇/璎珞/金步摇 · Lighting 烛光/月色/灵光/琉璃灯

**赛博朋克 / Cyberpunk**: Fabrics 记忆聚合物薄膜/凯夫拉纤维/光学迷彩涂层 · Materials 钛合金/全息神经矩阵/电致变色织物 · Garments 霓虹胶衣/全息裙/战术胸衣/夜光风衣 · Details 发光纹路/植入体/反射镜片/数据线

**西幻 / Western Fantasy**: Fabrics 秘银锁子甲/精灵魔藤纺线/深渊魔兽软皮 · Materials 星光蛛丝/水晶高跟/龙鳞 · Garments 法师长袍/精灵游侠装/暗夜贵族礼服/圣骑士铠甲(露腿甲片) · Details 附魔符文/魔力脉纹/月光石

**现代高定 / Modern High Fashion**: Fabrics 顶级桑蚕丝/真丝雪纺/法式重工蕾丝/高定羊绒 · Materials 铂金/碎钻/立体几何暗纹 · Cues 高定晚礼服/鸡尾酒裙/红毯/秀场后台

### 7.2 Style & atmosphere keywords

Gothic dark (shadows, candlelight, velvet, wrought iron, stained glass, chained chandelier) · Witchy/occult (potions, herbs, stars, pointed hat, wand, pentacle, candle circle) · Classical Chinese romance (纱衣半敞, incense, moonlight, boudoir, screen, pipa) · Modern glam (satin, high heels, champagne, chandeliers, city lights, mirrored ceiling) · Digital/cyber (neon grids, holograms, data streams, latex, wet-look, body chrome) · Dungeon/BDSM (red/black leather, chains, cage, suspension, industrial light) · Cottagecore (flowers, baskets, wood furniture, sunlight, nude in nature) · Bathhouse/onsen (stone, steam, water, wet skin, towel wrap, mountain) · Angel/fallen (white sheer robes, halo, wings, translucent layers) · Demon (red/black, horns, tail, leather, firelight, pentacle)

### 7.3 Classical Chinese beauty vocab

Beauty: 凝脂赛雪, 盈盈一握, 螓首蛾眉, 云鬓, 丹凤眼, 樱桃小口, 藕臂, 玉腿 · Fabrics: 绫罗绸缎, 绡纱, 薄纱, 锦缎, 缂丝 · Jewelry (仙侠饰词另见 §7.1): 珠钗, 玉镯, 金簪, 玉佩 · Architecture: 飞檐, 雕梁, 画栋, 回廊, 亭台, 水榭 · Nature: 梅花, 桃花, 牡丹, 翠竹, 流水, 假山

---

## 8. Props & Distinctive Details

- **Tech**: phone (selfie/text/scroll), laptop, headphones, camera, game controller, data cables
- **Drink/Food**: coffee cup, tea mug, wine glass, champagne flute, boba, street skewer, steamed bun, Popsicle
- **Bags**: tote, backpack, messenger, handbag, duffel, shopping bag, briefcase
- **Accessories**: glasses, scarf, hat, umbrella, watch, bracelet, choker, collar, O-ring, gag, blindfold
- **Bondage extras** (基础束缚硬件见 §2.8): paddle, flogger
- **Stationery**: book, notebook, pen, letter, envelope, fountain pen, scroll
- **Home**: keys, candle, incense burner, throw blanket, pillow, mug, wine glass
- **Nature**: flower, leaf, acorn, pinecone, seashell, cherry blossom
- **Classical**: fan (团扇/折扇), brush (毛笔), scroll (卷轴), go board (棋盘), zither (古琴), pipa (琵琶), ink stone (砚台)
- **Fantasy**: wand, potion vial, glowing crystal, ancient tome, spell book, magic rune, enchanted chains
- **Seasonal**: sakura branch, autumn leaf, snowball, ice skate, swimsuit, scarf, firework
- **Cat**: cat toy, laser pointer, feather wand, cardboard box, catnip, yarn ball
- **Professional**: stethoscope, clipboard, handcuffs, pointer stick, tray, mixing tools, cap

---

## 9. Aesthetic & Rendering Rules

- **Visual scanning order** — compose description in natural viewing progression: overall silhouette/style/posture → face & expression (gaze, blush, lips, ear) → collar & neckline (exposure, straps) → shoulder & sleeve (skin reveal, strap fall) → chest & torso (cleavage, bra/corset lines, drape) → waist & hip (belt, waistband, side slit) → legs & hosiery (sheerness, hem, garter, thigh compression) → feet & footwear (heel height, toe exposure, ankle strap)
- **Gatekeeping stance** (aesthetic confidence, not a filter to mention): youthful (<35) fair/warm-toned refined subject · non-human features limited to ears/horns/wings/tail · archetypes 极致御姐 / 高挑匀称 / 娇小玲珑
- **Context variables** — keep coherent: ① Geography/World ② Identity/Status (luxury ceiling, plausibility) ③ Micro-scene/privacy level (how much exposure is contextual) ④ Event/Purpose (seduction, relaxation, service, performance…)
- **Hosiery thickness** — descriptive only: 薄如蝉翼 gossamer / 极其轻透 ultra-sheer / 半透 semi-sheer / 微透 / 天鹅绒哑光 velvet matte (never "5D/30D")
- **Foot dorsum bare** — classic pumps (尖头细高跟/酒杯跟/玛丽珍…) keep the top of the foot uncovered; straps only at ankle or lower calf, never across the instep
