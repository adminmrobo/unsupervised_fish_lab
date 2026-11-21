# 표지 지시문 — 비지도학습 물고기 연구실 (unsupervised_fish_lab)

목차와 장마다 페이지 맨 위에 거는 표지 6장의 생성 지시문입니다. Genspark 등 이미지 생성 도구에 **위에서부터 순서대로** 붙여 넣으세요.

- 그림체: **16비트 RPG풍 픽셀아트 (필수, 고정)** — 매끈한 일러스트·벡터·수채화·3D로 나오면 다시 받습니다.
- 배경: **낮의 연구실·낮의 어시장** (흰 벽, 큰 창으로 드는 자연광). 밤·네온은 쓰지 않습니다.
- 참고 이미지(함께 올리기): 네 캐릭터 기본 그림 4장 — GitHub `adminmrobo/fruitfly-lab-expressions` (박사 E08, 조수 E13, 초파리 E10, 주판봇 v2 E13). **목차 표지(cover_00)를 먼저 받아** 그림체를 확인한 뒤, 나머지 다섯 장을 만들 때 cover_00도 참고 그림으로 함께 올립니다.
- 받은 그림은 `img/cover_00.webp` ~ `img/cover_05.webp`(1600×900, 220 KB 이하)로 넣으면 페이지가 대체 표지 대신 보여 줍니다. 같은 그림을 잘라 `thumb_NN.webp`(1200×800, 3:2)와 `og_NN.webp`(1200×630)도 만듭니다.

| 키 | 페이지 | 주제 은유 (글자 없이) | 앞 표지와 다르게 한 것 |
|---|---|---|---|
| cover_00 | index.html | 이름표를 뒤집어 덮은 물고기 상자의 뚜껑을 함께 여는 순간 | 어시장 입구 전경, 넷이 상자 하나를 둘러쌈 |
| cover_01 | 01_no_answer_key.html | 격자 매트 위 두 물고기 사이의 빛나는 점선(거리)과 같은 눈금의 자 여러 개(표준화) | 연구실 실험대, 위에서 내려다본 구도 |
| cover_02 | 02_grouping.html | 세 진열 주머니(초록·빨강·파랑 리본)에 체형별로 나뉜 물고기와 주머니 위에 꽂은 작은 깃발(중심) | 어시장 진열대 정면, 깃발을 꽂는 동작 |
| cover_03 | 03_folding.html | 손전등 빛이 물고기를 벽에 비춘 그림자(투영)와 바닥에 펼친 커다란 종이 지도 위 점들 | 넓은 바닥, 그림자와 지도 |
| cover_04 | 04_guessing.html | 천으로 덮어 가린 저울(가린 무게), 좁은 입구를 지나는 상자(병목), 낯선 큰 물고기 실루엣 앞에서 켜진 노란 경보등 | 검수 카운터, 경보등 |
| cover_05 | practice/index.html | 초록·파랑 손잡이가 달린 조작판과, 줄지어 지나가는 물고기 상자 위의 검수 아치 | 어시장 운영실 전경, 넷이 조작판 앞 |

**공통 영어 묘사 (모든 프롬프트에 그대로 들어 있음)**

- 박사: *chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie*
- 조수: *girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans*
- 초파리 연구원: *anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings*
- 주판봇: *boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus*
- 키 비율: 박사 1.00 · 조수 0.90 · 주판봇 0.72 · 초파리 0.41

---

## cover_00 · 목차 — 라벨링 없이 맞추는 AI

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_00 · L (16:9, 1920 이상) |
| 장소 | 낮의 어시장 입구, 흰 차양과 나무 상자 |
| 네 캐릭터 포즈 | 박사 가운데 뒤에서 상자 뚜껑을 들어 올림 / 조수 오른쪽 옆에서 상자 안을 들여다봄 / 초파리 왼쪽에서 오른쪽을 보며 뒤집힌 이름표 하나를 집어 듦 / 주판봇 오른쪽에서 왼쪽을 보며 주판을 듦 |
| 대체 글 (alt) | 연구실 식구 넷이 어시장 입구에서 이름표를 뒤집어 덮은 물고기 상자를 여는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- 비율 16:9, 가로 1920px 이상
- 그림체는 반드시 16비트 RPG풍 픽셀아트 (네모 픽셀이 보이게, 매끈한 일러스트·벡터·수채화·3D 금지)
- 첨부한 참고 이미지의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 외형으로, 넷 모두 픽셀아트로 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게
아래 영어 프롬프트를 그대로 써 줘.

Website top cover illustration, wide 16:9.
Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2-3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.
Match the characters' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style. Height ratio: doctor 1.00, girl 0.90, robot 0.72, fruit fly 0.41.
Scene: the entrance of a bright daytime fish market, white canopies, wooden crates, natural light, white walls with small lavender, mint and pink accents.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, center back, lifting the lid of a big wooden fish crate;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, on the right side of the crate, peeking inside with curiosity;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, holding up one blank paper tag that was turned face-down;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left.
Visual metaphor of the topic: many silver fish inside the crate with all their paper tags turned face-down and blank, so nobody can see the names.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain, bright and simple; the light falls on the open crate.
Mood: curious, friendly rivalry, the moment before the result.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

## cover_01 · 1장 — 정답표 없이 배운다 (거리와 표준화)

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_01 · L |
| 장소 | 낮의 연구실 실험대, 위에서 비스듬히 내려다본 구도 |
| 네 캐릭터 포즈 | 박사 가운데 뒤에서 두 물고기 사이를 손으로 가리킴 / 조수 옆에서 같은 눈금의 자 여러 개를 가지런히 늘어놓음 / 초파리 왼쪽에서 오른쪽을 보며 돋보기로 점선을 살핌 / 주판봇 오른쪽에서 왼쪽을 보며 큰 저울을 자랑스럽게 가리킴 |
| 대체 글 (alt) | 격자 매트 위 두 물고기 사이에 빛나는 점선이 이어지고, 조수가 같은 눈금의 자를 늘어놓는 실험대 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘. (cover_00과 같은 그림체, 첨부한 cover_00도 참고)
- 비율 16:9, 가로 1920px 이상, 16비트 RPG풍 픽셀아트, 글자·숫자·로고 없음
- 네 캐릭터 모두 참고 이미지와 같은 외형
아래 영어 프롬프트를 그대로 써 줘.

Website top cover illustration, wide 16:9.
Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2-3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.
Match the characters' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style.
Scene: a bright daytime laboratory workbench seen slightly from above, a large mint grid mat on the table, big window light.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, center back, pointing between two fish on the mat;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, lining up several identical wooden rulers with the same tick marks side by side;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, inspecting the dotted line with a magnifying glass;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, on the right facing left, proudly pointing at a big kitchen scale.
Visual metaphor of the topic: two fish of different sizes lying on the grid mat, connected by one glowing dotted straight line (distance), plus a row of identical rulers (same scale for every measurement).
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain, bright and simple; the light falls on the glowing dotted line.
Mood: curious, friendly rivalry, the moment before the result.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

## cover_02 · 2장 — 묶기 (군집화)

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_02 · L |
| 장소 | 낮의 어시장 진열대 정면, 흰 타일과 나무 선반 |
| 네 캐릭터 포즈 | 박사 가운데 뒤에서 작은 깃발을 주머니 위에 꽂음 / 조수 옆에서 물고기를 두 손으로 주머니에 옮겨 담음 / 초파리 왼쪽에서 오른쪽을 보며 주머니 경계의 물고기 한 마리를 가리킴 / 주판봇 오른쪽에서 왼쪽을 보며 빈 주머니 여러 개를 더 끌고 옴 |
| 대체 글 (alt) | 어시장 진열대의 세 주머니에 납작한 물고기, 중간 물고기, 길쭉한 물고기가 나뉘어 담기고 박사가 주머니마다 깃발을 꽂는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘. (cover_00과 같은 그림체, 첨부한 cover_00도 참고)
- 비율 16:9, 가로 1920px 이상, 16비트 RPG풍 픽셀아트, 글자·숫자·로고 없음
- 네 캐릭터 모두 참고 이미지와 같은 외형
아래 영어 프롬프트를 그대로 써 줘.

Website top cover illustration, wide 16:9.
Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2-3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.
Match the characters' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style.
Scene: the front of a bright daytime fish market display counter, white tiles, wooden shelves, natural light.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, center back, planting a small flag on top of one cloth sack;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, carefully moving a fish into a sack with both hands;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, pointing at one fish lying between two sacks;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, on the right facing left, dragging in a stack of many more empty sacks.
Visual metaphor of the topic: three open cloth sacks with green, red and blue ribbons; one holds tall flat-bodied fish, one holds medium fish, one holds long slender fish; a small flag stands on each sack.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain, bright and simple; the light falls on the three sacks.
Mood: curious, friendly rivalry, the moment before the result.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

## cover_03 · 3장 — 접기 (차원 축소)

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_03 · L |
| 장소 | 낮의 연구실 넓은 바닥과 흰 벽 |
| 네 캐릭터 포즈 | 박사 가운데 뒤에서 손전등으로 물고기를 비춤 / 조수 바닥의 큰 종이 지도 위에 무릎 꿇고 점을 찍음 / 초파리 왼쪽에서 오른쪽을 보며 벽의 그림자를 가리킴 / 주판봇 오른쪽에서 왼쪽을 보며 여섯 갈래 색실 뭉치를 안고 있음 |
| 대체 글 (alt) | 박사가 손전등으로 물고기를 비춰 흰 벽에 그림자가 생기고, 조수가 바닥의 큰 종이 지도에 점을 찍는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘. (cover_00과 같은 그림체, 첨부한 cover_00도 참고)
- 비율 16:9, 가로 1920px 이상, 16비트 RPG풍 픽셀아트, 글자·숫자·로고 없음
- 네 캐릭터 모두 참고 이미지와 같은 외형
아래 영어 프롬프트를 그대로 써 줘.

Website top cover illustration, wide 16:9.
Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2-3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.
Match the characters' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style.
Scene: a bright daytime laboratory with a wide floor and a plain white wall, big window light.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, center back, shining a flashlight at a fish held on a stand;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, kneeling on a huge paper map spread on the floor, placing small colored dots;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, pointing at the fish shadow on the wall;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, on the right facing left, hugging a bundle of six colored threads.
Visual metaphor of the topic: a three-dimensional fish casting a flat two-dimensional shadow on the white wall (projection), and a floor map whose dots form two long diagonal bands.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain, bright and simple; the light falls on the shadow on the wall.
Mood: curious, friendly rivalry, the moment before the result.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

## cover_04 · 4장 — 맞히기 (자기지도학습)

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_04 · L |
| 장소 | 낮의 어시장 검수 카운터 |
| 네 캐릭터 포즈 | 박사 가운데 뒤에서 저울을 덮은 천을 살짝 들춤 / 조수 옆에서 좁은 입구가 달린 상자에 물고기 카드를 넣음 / 초파리 왼쪽에서 오른쪽을 보며 켜진 노란 경보등을 가리킴 / 주판봇 오른쪽에서 왼쪽을 보며 커다란 낯선 물고기 실루엣을 당당히 맞이함 |
| 대체 글 (alt) | 검수 카운터에서 박사가 천으로 덮은 저울을 들추고, 초파리 연구원이 낯선 큰 물고기 앞에서 켜진 경보등을 가리키는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘. (cover_00과 같은 그림체, 첨부한 cover_00도 참고)
- 비율 16:9, 가로 1920px 이상, 16비트 RPG풍 픽셀아트, 글자·숫자·로고 없음
- 네 캐릭터 모두 참고 이미지와 같은 외형
아래 영어 프롬프트를 그대로 써 줘.

Website top cover illustration, wide 16:9.
Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2-3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.
Match the characters' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style.
Scene: an inspection counter in a bright daytime fish market, white tiles, a measuring board on the counter, natural light.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, center back, lifting a corner of a cloth that covers a scale;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, sliding a fish card into a box that has a very narrow slot in the middle;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, pointing at a lit yellow warning lamp;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, on the right facing left, confidently welcoming the silhouette of an unusually huge fish at the doorway.
Visual metaphor of the topic: a scale hidden under a cloth (the masked value), a box with a narrow bottleneck slot, and a yellow warning lamp glowing beside an unfamiliar oversized fish silhouette.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain, bright and simple; the light falls on the covered scale and the warning lamp.
Mood: curious, friendly rivalry, the moment before the result.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

## cover_05 · 마지막 장 — 실전 연습장 (어시장 운영 시뮬레이터)

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_05 · L |
| 장소 | 낮의 어시장 운영실, 큰 창 너머로 진열대와 물고기 상자 줄이 보임 |
| 네 캐릭터 포즈 | 박사 가운데 뒤에서 팔짱 끼고 운영판을 지켜봄 / 조수 옆에서 파란 손잡이를 돌림 / 초파리 왼쪽에서 오른쪽을 보며 초록 손잡이 옆 계기를 확인 / 주판봇 오른쪽에서 왼쪽을 보며 모든 손잡이를 최대로 올리려 함 |
| 대체 글 (alt) | 어시장 운영실에서 연구실 식구 넷이 초록·파랑 손잡이가 달린 조작판 앞에 모여 물고기 상자 줄과 검수 아치를 내려다보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘. (cover_00과 같은 그림체, 첨부한 cover_00도 참고)
- 비율 16:9, 가로 1920px 이상, 16비트 RPG풍 픽셀아트, 글자·숫자·로고 없음
- 네 캐릭터 모두 참고 이미지와 같은 외형
아래 영어 프롬프트를 그대로 써 줘.

Website top cover illustration, wide 16:9.
Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2-3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.
Match the characters' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style.
Scene: a bright daytime control room above a fish market; through a big window you can see display counters and a conveyor line of fish crates passing under an inspection arch with a small lamp.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, center back, arms crossed, watching the panel;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, turning a blue knob on the control panel;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, checking a gauge next to a green knob;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, on the right facing left, trying to push every slider to the maximum.
Visual metaphor of the topic: a control panel with green knobs (market conditions) and blue knobs (my decisions), and the line of fish crates passing the inspection arch outside.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain, bright and simple; the light falls on the control panel.
Mood: curious, friendly rivalry, the moment before the result.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

**고칠 때 (같은 대화에서):** `Same four characters, same 16-bit pixel-art style and composition. Change only: {고칠 점}. Still pixel art, still no text.`
