# King John 1205: Game Design Document

**Version:** 1.0
**Date:** January 18, 2026
**Project Type:** Text-based historical adventure game
**Target Platform:** Python (terminal), future web port

---

## 1. Executive Summary

King John 1205 is a day-by-day historical simulation/text adventure where players experience a pivotal year in the life of King John of England. The year 1205 was marked by military preparations, baronial tensions, church conflicts, and constant royal movement. Players will make strategic, administrative, and personal decisions as King John, managing resources and relationships while navigating historical events.

**Core Experience:** Strategic decision-making in a historical context with meaningful consequences, narrative branching, and resource management.

**Target Audience:** History enthusiasts, strategy gamers, interactive fiction fans

**Estimated Playtime:** 8-15 hours for complete playthrough

---

## 2. Game Vision

### 2.1 Design Pillars

1. **Historical Immersion** - Players experience medieval kingship authentically, with period-accurate language, concerns, and constraints
2. **Meaningful Choice** - Every decision has weight and consequences that ripple through the year
3. **Strategic Depth** - Balancing multiple competing resources and relationships requires planning
4. **Emergent Narrative** - Player choices create their own version of 1205, compared against history

### 2.2 Core Gameplay Loop

```
Morning Reports → Review Situation → Make Decisions →
See Consequences → Evening Events → Next Day
```

Each day advances the calendar from January 1 to December 31, 1205.

### 2.3 Tone and Style

- **Serious but accessible** - Historical without being dry
- **Medieval voice** - Period-appropriate language without being archaic
- **Human drama** - Focus on personalities, conflicts, and ambitions
- **Consequential** - Actions matter, creating tension and investment

---

## 3. Core Gameplay Systems

### 3.1 Resource Management System

Resources are the quantitative measure of the kingdom's health and the king's power.

#### 3.1.1 Primary Resources (0-100 scale unless noted)

| Resource | Range | Description | Critical Thresholds |
|----------|-------|-------------|---------------------|
| **Treasury** | 0-20,000 marks | Available royal funds for military, bribes, building | <2,000: Financial crisis; <500: Bankruptcy |
| **Papal Relations** | -100 to +100 | Relationship with Pope Innocent III | <-30: Strained; <-60: Interdict risk; <-80: Excommunication |
| **Military Readiness** | 0-100 | Preparedness of forces, fleet, fortifications | <30: Vulnerable to invasion; >80: Strong deterrent |
| **Royal Authority** | 0-100 | Overall legitimacy and power of the crown | <30: Widespread defiance; <15: Civil war risk |

#### 3.1.2 Baronial Relationships (0-100 each)

Individual nobles whose loyalty must be maintained:

- **William Marshal** (Earl of Pembroke) - Most powerful baron, moral authority, cautious
- **William Longespée** (Earl of Salisbury) - Your half-brother, military leader, loyal but proud
- **William de Braose** - Marcher lord, ambitious, historically falls from favor
- **Geoffrey FitzPeter** - Justiciar (chief administrator), pragmatic, essential
- **Roger de Lacy** - Northern/Marcher power, controls key territory
- **Robert de Vieuxpont** - Northern baron, sheriff of multiple counties
- **William de Stuteville** - Yorkshire magnate, important for northern stability
- **Hugh de Neville** - Chief Forester, controls significant patronage

**Relationship Mechanics:**
- **>70:** Loyal - actively supports you, gives good counsel
- **50-69:** Neutral - fulfills obligations, watches carefully
- **30-49:** Discontented - passive resistance, requires attention
- **<30:** Hostile - may rebel, withholds service, plots

**Derived Metric:** Average Baronial Loyalty (sum of all / count)

#### 3.1.3 Regional Stability (0-100 each)

Geographic areas requiring management:

- **Southern England** - Core royal domain (Winchester, Westminster, Portsmouth)
- **Northern England** - Yorkshire, Northumberland, historically independent-minded
- **Welsh Marches** - Border region, frequent conflicts with Welsh princes
- **Scotland Border** - Relations with King William of Scotland
- **Ireland** - English holdings, requires attention and military presence
- **Continental Holdings** - Poitou, Gascony (all that remains after Normandy's loss)

**Stability Mechanics:**
- **>70:** Peaceful - tax collection efficient, military levies reliable
- **50-69:** Settled - Normal governance, occasional issues
- **30-49:** Unstable - Unrest, reduced revenue, military distractions
- **<30:** Crisis - Rebellion, invasion, or collapse imminent

**Derived Metric:** Overall Kingdom Stability (weighted average, Southern England counts double)

#### 3.1.4 Resource Interactions

Resources influence each other:

```
Example Interaction Web:
- Low Treasury → Cannot pay troops → Military Readiness drops
- Low Baronial Loyalty → Regional Stability drops → Tax revenue decreases
- High Royal Authority → Better baronial loyalty → More military service
- Negative Papal Relations → Church withholds support → Authority drops
```

### 3.2 Calendar and Time System

#### 3.2.1 Date Tracking

- Game spans January 1 - December 31, 1205 (365 days)
- Medieval calendar with feast days marked (Epiphany, Easter, Pentecost, Christmas, etc.)
- Day of week tracked (important for religious observances)
- Historical events tied to specific dates

#### 3.2.2 Location and Travel

King John was constantly mobile in 1205. The game tracks:

- **Current Location** - One of 40+ locations (castles, cities, monasteries)
- **Travel Time** - Days required to move between locations
- **Travel Events** - Random encounters, opportunities during transit

Major Locations:
- Westminster/London (political center)
- Winchester (old capital, treasury)
- Windsor, Woodstock (favorite residences)
- Portsmouth, Portchester (naval bases)
- Canterbury (church center)
- Nottingham, York (northern strongholds)
- Bristol (western port)
- Marlborough, Clarendon (hunting lodges)

### 3.3 Multi-Phase Daily Structure

Each day unfolds in 4 phases:

#### Phase 1: Morning Reports
- **Display:** Date, location, weather/season flavor
- **Reports:** Overnight intelligence, treasury updates, urgent messages
- **Resource Dashboard:** All current values displayed
- **Duration:** Read-only, player absorbs information

#### Phase 2: Decision Time
- **Primary Event:** Main scripted, triggered, or random event (70% of days)
- **Administrative Options:** Routine matters requiring approval (50% of days)
- **Personal/Social:** Leisure, family time, religious observance (30% of days)
- **Review Options:** Consult advisors, check relationships, read journal
- **Player Choice:** Select one action (or pass/rest if no urgent matter)

#### Phase 3: Resolution
- **Outcome:** Narrative result of chosen action
- **Resource Changes:** Clear display of +/- changes with color coding
- **Consequences:** Immediate and flagged future consequences
- **Advisor Reactions:** Key barons/advisors comment if relevant

#### Phase 4: Evening/Random Events
- **Random Events:** 20% chance per day for unexpected event
- **Multi-Day Progressions:** Ongoing event chains advance
- **Travel Progress:** If traveling, show movement
- **Optional:** Player can rest, consult advisors again, or continue

#### Special Day Types

- **Travel Days:** Compressed - "3 days pass as you journey to York"
- **Multi-Day Events:** Only show detailed phases on key decision days
- **Quiet Periods:** Option to skip ahead through routine days (with summary)
- **Crisis Days:** Extended phases, multiple urgent decisions

### 3.4 Event System

#### 3.4.1 Event Types

**Historical Anchor Events (60 total)**
- Tied to specific dates from historical record
- Major turning points that "must" happen (but player influences HOW)
- Examples:
  - Death of Archbishop Hubert Walter (July 13)
  - Pentecost Invasion Decision (June 5)
  - Christmas Court at Oxford (December 25)

**Triggered Events (40 total)**
- Condition-based, fire when criteria met
- Examples:
  - Treasury < 2,000 → Tax revolt triggers
  - William Marshal relationship < 30 → He demands audience
  - Welsh Marches < 40 → Border raid occurs
  - Royal Authority > 80 + Military > 75 → Opportunity for Scottish campaign

**Event Templates (30 templates)**
- Repeatable structures with variable content
- Examples:
  - Petitioner Requests Charter [location, person, request vary]
  - Intelligence Report from [France/Wales/Scotland/Ireland]
  - Social Occasion [hunt/feast/tournament]
  - Religious Request [monastery wants donation/privilege]

**Random Events (50 total)**
- Pool of unexpected events, drawn randomly
- Add variety and unpredictability
- Examples:
  - Merchant ship captured by pirates
  - Severe weather damages castle
  - Unexpected diplomatic envoy arrives
  - Noble's scandalous behavior requires response

**Multi-Day Event Chains (20 chains)**
- Extended scenarios spanning 5-15 days
- Major historical moments expanded into full arcs
- Examples:
  - The Pentecost Invasion Crisis (10 days, June 1-10)
  - Archbishop Succession Struggle (15 days, July-August)
  - Northern Progress and Scottish Negotiation (12 days, October-November)
  - Christmas Court Preparation and Celebration (7 days, December 20-26)

#### 3.4.2 Event Structure

Every event contains:

```yaml
event_id: unique_identifier
type: [historical, triggered, random, chain]
title: "Event Title"
date: [specific, conditional, or null]
location: [specific, conditional, or null]
description: "Narrative setup text"
conditions:
  - resource_requirements
  - flag_requirements
  - date_requirements
choices:
  - choice_id: 1
    text: "Choice text"
    requirements: [optional prerequisites to select this]
    consequences:
      resources: {treasury: -500, authority: +5}
      relationships: {william_marshal: -5}
      regions: {welsh_marches: +3}
      flags: [choice_1_taken]
    narrative_outcome: "Result text"
  - choice_id: 2
    [...]
advisors:
  - advisor: william_marshal
    advice: "Marshal's counsel"
    bias: [cautious, honor-focused]
historical_context: "What really happened"
historical_outcome: [flag indicating historical path]
```

#### 3.4.3 Event Frequency

Target distribution across 365 days:

- **Historical Anchors:** 60 events (16%)
- **Multi-Day Chains:** 20 chains × avg 3 decision days = 60 days (16%)
- **Triggered Events:** ~40 across the year (11%)
- **Templates/Random:** ~100 days (27%)
- **Quiet Days (minor/auto-resolved):** ~105 days (29%)

This ensures variety while preventing player fatigue.

### 3.5 Advisor System

Five key advisors provide counsel and perspective:

#### William Marshal (Military Advisor)
- **Personality:** Cautious, honorable, experienced
- **Expertise:** Military strategy, feudal obligations, chivalric code
- **Bias:** Prefers diplomatic solutions, wary of risky campaigns
- **Trigger:** Warns when Military Readiness low, or when contemplating aggressive action

#### Geoffrey FitzPeter (Administrative Advisor)
- **Personality:** Pragmatic, detail-oriented, loyal administrator
- **Expertise:** Finance, law, bureaucracy
- **Bias:** Focuses on practical considerations, treasury impact
- **Trigger:** Alerts when Treasury low, when administrative efficiency matters

#### John de Gray (Church Advisor)
- **Personality:** Ambitious, politically savvy, loyal to John
- **Expertise:** Church politics, papal relations, religious law
- **Bias:** Your candidate for Archbishop, advises asserting royal authority over church
- **Trigger:** Papal Relations dropping, church matters, Archbishop succession

#### Intelligence Officer (Scout/Spy - Generic)
- **Personality:** Professional, neutral reporter
- **Expertise:** Foreign intelligence, military movements, rumors
- **Bias:** None, presents facts
- **Trigger:** Reports from France, Wales, Scotland, Ireland

#### Queen Isabella (Family/Personal Advisor)
- **Personality:** Young, politically astute, protective of children
- **Expertise:** Court politics, noble relationships, family matters
- **Bias:** Focuses on dynastic security, preservation of Angoulême connection
- **Trigger:** Family matters, social events, noble relationship issues

**Advisor Mechanics:**
- Available via "Consult Advisors" option in Phase 2
- Provide advice on current situations (often different perspectives)
- Their relationship values influence advice quality and willingness to help
- Low relationship → advisor may be brief, unhelpful, or subtly undermining

---

## 4. Narrative Design

### 4.1 Historical Fidelity Framework

**Hybrid Approach:** Historical anchors + player agency

#### Fixed Elements (Cannot Be Changed)
- Death of Archbishop Hubert Walter (July 13, 1205)
- Loss of Normandy already occurred (1204 - game context)
- Calendar dates and religious feasts
- Core NPC personalities and historical relationships
- Geographic reality (travel times, locations)

#### Player-Influenced Elements
- **Pentecost Invasion:** Can it succeed? (historically cancelled)
  - Success Path: Requires high Military Readiness + Baronial Loyalty + Treasury
  - Changes July-December events (you're in France vs. England)
  - Narrow path - difficult but possible

- **Archbishop Succession:** Can you install John de Gray vs. Stephen Langton?
  - Success requires high Papal Relations or extreme political pressure
  - Affects church-state relations for rest of year

- **Baronial Loyalty:** Can you prevent the seeds of rebellion?
  - High loyalty at year end → no Magna Carta in future
  - Unlock "prevented Magna Carta" alternate ending

- **William de Braose:** Can you keep him loyal or does he fall?
  - Historical: He falls from grace and flees
  - Player can maintain relationship with careful handling

#### Alternate Timeline Handling

Major divergences create branching paths:

**Successful Invasion Branch:**
- June-August: Campaign in Normandy (alternate event set)
- September: Return to England for governance
- Consequences: Higher authority, treasury drain, different baronial reactions
- Historical accuracy score decreases but "Military Victor" achievement unlocks

**Failed Invasion Branch (Historical):**
- June-December: Focus on English governance, defense prep
- Baronial resentment grows
- Sets stage for future conflicts
- Higher historical accuracy score

### 4.2 Win Conditions and Endings

#### Survival Baseline
- Reach December 31, 1205 without game over
- Game over triggers:
  - Treasury < 0 for 30 days (bankruptcy)
  - Royal Authority < 10 (rebellion/civil war)
  - Average Baronial Loyalty < 15 (mass defection)
  - All regions < 25 stability (kingdom collapse)

#### End-of-Year Scoring

**Final Score Calculation:**
```
Total Score =
  (Treasury / 100) +
  (Royal Authority × 5) +
  (Average Baronial Loyalty × 3) +
  (Military Readiness × 2) +
  (Papal Relations + 100) / 2 +
  (Kingdom Stability × 3) +
  Achievement Bonuses +
  Historical Accuracy Bonus (if close to history)
```

**Score Bands:**
- 1000+: "John the Great" - Exceptional rule
- 800-999: "John the Reformer" - Strong kingship
- 600-799: "John the Capable" - Adequate rule
- 400-599: "John Lackland" - Struggling monarch
- 200-399: "John Softsword" - Weak rule
- <200: "John the Tyrant" - Disaster

#### Achievement System

**Military Achievements:**
- "Conqueror" - Successfully launch Pentecost invasion
- "Defender of the Realm" - Maintain Military Readiness > 80 all year
- "Naval Supremacy" - Build 60+ galleys

**Political Achievements:**
- "Prevented Magna Carta" - End with Average Baronial Loyalty > 75
- "Master of England" - All regions > 75 stability
- "Church Victor" - Install John de Gray as Archbishop

**Personal Achievements:**
- "The Restless King" - Visit 30+ locations
- "Historical Path" - Make historically accurate choices (>80%)
- "Alternate Timeline" - Major divergence from history
- "Royal Diplomat" - Maintain all baron relationships > 50

**Special Endings:**
- Based on unique flag combinations
- Example: High authority + low loyalty = "The Feared King" ending
- Example: Low papal relations + high baronial loyalty = "Protestant King" ending (anachronistic humor)

### 4.3 Tone and Writing Guidelines

**Voice:**
- Third-person limited (from John's perspective)
- Present tense for immediacy
- Period vocabulary without being inaccessible
- Example: "The Marshal enters your chamber, his weathered face grave. 'My lord, the barons grow restless. Your taxation weighs heavy upon them.'"

**Length:**
- Event descriptions: 100-300 words
- Choices: 10-25 words each
- Outcomes: 50-150 words
- Daily summaries: 20-50 words

**Historical Context:**
- Events include optional "Historical Note" for educational value
- Available via "Learn More" option during events
- Example: "Historically, John demanded hostages from William Marshal's family to ensure loyalty - a practice that would contribute to baronial grievances leading to Magna Carta."

---

## 5. Progression and Pacing

### 5.1 Year Structure

The year follows a dramatic arc:

**Act 1: January-March (Days 1-90) - "Preparation"**
- Setting up the invasion
- Establishing baseline relationships
- Tutorial period (lighter consequences)
- Introduce core systems gradually

**Act 2: April-June (Days 91-181) - "Crisis"**
- Build to Pentecost invasion decision
- Baronial tensions escalate
- Resource pressure increases
- Major branching point (invasion succeeds/fails)

**Act 3: July-September (Days 182-273) - "Aftermath"**
- Deal with invasion consequences
- Archbishop Hubert Walter dies (major church crisis)
- Military expeditions or defensive posture
- Triggered events more frequent

**Act 4: October-December (Days 274-365) - "Resolution"**
- Northern progress and diplomatic efforts
- Consolidation of position
- Christmas court (reflection and ceremony)
- Setup for next year (1206)
- Final scoring and endings

### 5.2 Difficulty Curve

**Early Game (Jan-Mar):**
- Resources start moderate (Treasury 8,000, Authority 65, etc.)
- Easier choices with clear good/bad options
- Fewer simultaneous pressures
- Tutorial tooltips and explanations

**Mid Game (Apr-Sep):**
- Multiple competing pressures
- Trade-offs become harder
- Resource drain increases
- Triggered events add complexity

**Late Game (Oct-Dec):**
- Consequences of early choices manifest
- Difficult resource recovery if low
- Opportunity for triumph or desperate survival
- High-stakes decisions

### 5.3 Replayability

**Factors encouraging replay:**
- Multiple paths through major events (invasion, archbishop, etc.)
- Different relationship strategies (favor different barons)
- Achievement hunting
- Historical accuracy challenge vs. alternate history playstyle
- Random event variation
- Different starting difficulty levels (future enhancement)

---

## 6. User Interface

### 6.1 Main Menu
```
╔══════════════════════════════════════════════╗
║     KING JOHN 1205: A ROYAL CHRONICLE      ║
╚══════════════════════════════════════════════╝

1. New Game
2. Continue Game
3. Load Game
4. Settings
5. Historical Context (about 1205)
6. Credits
7. Exit

Your choice:
```

### 6.2 Resource Dashboard
```
═══════════════════════════════════════════════════════════════
Day 152 - Thursday, May 31, 1205 - Portsmouth
═══════════════════════════════════════════════════════════════

RESOURCES:
Treasury: 8,450 marks        Military Readiness: 78/100 ▓▓▓▓▓▓▓░░
Royal Authority: 71/100      Papal Relations: 35/100 ▓▓▓░░░░░░░

BARONIAL LOYALTY (Average: 62/100):
W.Marshal: 68  W.Longespée: 75  W.de Braose: 45  G.FitzPeter: 70
R.de Lacy: 58  R.de Vieuxpont: 60  W.de Stuteville: 55  H.de Neville: 65

REGIONAL STABILITY (Overall: 64/100):
South: 78  North: 55  Welsh Marches: 48  Scotland: 60  Ireland: 52  Continent: 58

[Press 'D' for detailed view | 'A' for advisors | 'J' for journal]
═══════════════════════════════════════════════════════════════
```

### 6.3 Event Presentation
```
═══════════════════════════════════════════════════════════════
                    THE PENTECOST FLEET
═══════════════════════════════════════════════════════════════

Your fleet lies at anchor in Portsmouth harbor, fifty galleys and
twice that many transports. The army you've assembled—knights,
serjeants, and Flemish mercenaries—waits aboard or camps on the
shore. Today is Pentecost, the date you set for your great
enterprise: the reconquest of Normandy.

Yet your tent is heavy with tension. This morning, William Marshal
and several great barons came to you with grave concerns. They
speak of leaving England defenseless, of their own Norman lands
already lost, of the risk of Philip's superior forces. Some refuse
outright to sail.

Marshal stands before you: "My lord, I counsel caution. We have
not the strength to hold Normandy even if we take it. Better to
secure England first."

Your half-brother Longespée counters: "We must strike now, before
Philip consolidates! Give the order to sail, sire."

[Historical Context: Historically, John cancelled the invasion due
to baronial refusal. Only a small force under Longespée sailed to
Poitou later in the year.]

YOUR DECISION:

1. Order the fleet to sail immediately - You are King, they will obey
   [Requires: Authority > 70, Military > 75]

2. Sail with a reduced force of loyalists only
   [Moderate resources, less risky]

3. Cancel the invasion and punish those who refused
   [Assert authority but lose military opportunity]

4. Cancel and accept their counsel gracefully
   [Historical path, maintain relationships]

5. Consult advisors for more opinions

Your choice:
```

### 6.4 Color Coding (Terminal)
- **Green:** Positive resource changes, good news
- **Red:** Negative changes, warnings, crises
- **Yellow:** Neutral information, moderate concerns
- **Blue:** Location names, dates, proper nouns
- **Cyan:** Advisor names and dialogue
- **Magenta:** Historical notes, achievements

### 6.5 Journal System
```
╔══════════════════════════════════════════════╗
║             ROYAL JOURNAL                    ║
╚══════════════════════════════════════════════╝

Showing: Last 10 events | [F]ilter | [S]earch | [B]ack

Day 152 (May 31, 1205) - Portsmouth
  » Pentecost Fleet Decision
    Choice: Cancelled invasion, punished refusers
    Treasury -300, Authority +5, W.Marshal -10

Day 148 (May 27, 1205) - Portsmouth
  » Merchant Petition for Wine License
    Choice: Granted for fee
    Treasury +50

Day 145 (May 24, 1205) - Canterbury
  » Bishop's Council on French Threat
    Choice: Committed to defensive strategy
    Military Readiness +3, South England +5

[... etc ...]
```

---

## 7. Technical Requirements

### 7.1 Platform Requirements

**Initial Release (Python Terminal):**
- Python 3.9+
- Standard library only (no external dependencies initially)
- Cross-platform (Windows, Mac, Linux)
- Terminal with 80+ column width
- Optional: colorama for Windows color support

**Future Port (Web):**
- HTML5/JavaScript or React
- Browser-based, no installation
- Mobile-responsive design
- Save system via localStorage or database

### 7.2 Performance Targets
- Game load time: < 2 seconds
- Save/load operations: < 1 second
- Event processing: Instant (<100ms)
- Memory footprint: < 50MB

### 7.3 Save System
- Auto-save at end of each day
- Manual save anytime
- Multiple save slots (5 slots)
- Save data includes:
  - Current date
  - All resource values
  - All relationship values
  - All flags/state
  - Event history
  - Location and travel state

### 7.4 Data Format
- Initial: Python dictionaries in .py files
- Migration: JSON files for easier editing
- Save files: JSON format
- Event validation on load (prevent corruption)

---

## 8. Content Guidelines

### 8.1 Historical Accuracy Standards

**Primary Source:** The provided PDF document "King John's Movements and Activities in 1205"

**Research Approach:**
- Events should be grounded in historical record where possible
- Personalities based on chronicler accounts and modern scholarship
- When inventing content (daily filler), ensure period-appropriateness
- Anachronisms avoided except for gameplay clarity

**Historical Context Notes:**
- Every major event should include optional historical note
- Cite sources when possible (e.g., "According to Roger of Wendover...")
- Educational value without being pedantic

### 8.2 Writing Style Guide

**DO:**
- Use active voice and present tense
- Create dramatic tension
- Show character through dialogue
- Ground abstract concepts in concrete details
- Make player feel weight of decisions

**DON'T:**
- Use modern slang or concepts
- Make decisions obvious (no clear "good" choice always)
- Info dump historical context in main narrative
- Write overly long descriptions
- Use archaic language that confuses (no "ye olde")

**Example Good Writing:**
> Marshal's jaw tightens. "My lord, you ask us to cross the Channel with half an army while Philip commands thrice our number. This is folly." Around the tent, barons nod agreement. Your authority is being tested.

**Example Bad Writing:**
> Verily, Sir William doth protest thy strategic endeavor, milord. Forsooth, 'twould be most unwise to embark upon this venture across ye waters.

### 8.3 Choice Design Principles

**Every choice should:**
1. Be meaningful (not illusion of choice)
2. Have trade-offs (rarely a strictly best option)
3. Reflect character/values (cautious, aggressive, pious, pragmatic)
4. Have clear immediate and possible long-term consequences
5. Be understandable without meta-gaming

**Choice Categories:**
- **Strategic:** Long-term planning, major decisions
- **Tactical:** Immediate problems, reactive
- **Diplomatic:** Relationship management, negotiation
- **Administrative:** Routine governance, efficiency
- **Personal:** Character development, values

**Avoid:**
- Obvious traps (choices that are clearly terrible)
- False choices (all lead to same outcome)
- Required foreknowledge (can't succeed without external info)
- Unclear consequences (player should reasonably predict)

---

## 9. Scope and Constraints

### 9.1 Must-Have Features (Phase 1-3)
- Complete resource system (18 tracked values)
- Multi-phase daily structure
- 60 historical anchor events
- Save/load system
- Basic UI with dashboard
- Advisor consultation
- End-of-year scoring

### 9.2 Should-Have Features (Phase 4-5)
- All event types (triggered, random, templates, chains)
- Complete journal/history system
- Achievement tracking
- Multiple endings
- Enhanced UI with color
- Historical notes on all major events

### 9.3 Nice-to-Have Features (Phase 6 / Future)
- Difficulty levels
- Custom game options (start with different resources)
- ASCII art map
- Character portraits (text art)
- Sound effects (terminal beeps for events)
- Export playthrough to text file
- Modding support (JSON event files)

### 9.4 Explicitly Out of Scope
- Graphics (terminal only, possible web port later)
- Multiplayer
- Years beyond 1205 (future sequel potential)
- Combat minigames or real-time elements
- Voice acting
- Extensive character customization (you are John, not custom character)

---

## 10. Success Metrics

### 10.1 Development Milestones

**Milestone 1: Core Loop (Week 3)**
- One complete day cycle functional
- All four phases implemented
- Placeholder event works
- Resources update correctly

**Milestone 2: Vertical Slice (Week 7)**
- 10-15 real events playable
- One multi-day chain complete
- Save/load working
- Alpha playtest ready

**Milestone 3: Content Complete (Week 12)**
- All 60 historical events implemented
- All event types functional
- Full year playable start-to-finish
- Beta playtest ready

**Milestone 4: Polish Complete (Week 15)**
- UI polished
- Balancing complete
- All features implemented
- Release candidate

### 10.2 Quality Standards

**Code Quality:**
- Documented functions and classes
- Consistent naming conventions
- Modular, maintainable structure
- No game-breaking bugs

**Content Quality:**
- All events proofread
- Historical accuracy verified
- Choice consequences balanced
- Playable without wiki/guide

**User Experience:**
- Clear UI feedback
- Intuitive navigation
- Helpful tooltips
- Satisfying progression

---

## 11. Future Expansion Possibilities

### Post-Launch Content
- Additional event packs (more variety in random pool)
- "What If" scenarios (John wins at Pentecost, etc.)
- Character-focused DLC (play as William Marshal)
- Subsequent years (1206, 1207... to Magna Carta 1215)

### Technical Enhancements
- Web version with visual UI
- Mobile apps
- Achievement/stat tracking across playthroughs
- Community event sharing

### Game Modes
- Story Mode (current design)
- Historical Challenge (strict accuracy required)
- Sandbox Mode (custom starting resources)
- Ironman Mode (no reloading saves)

---

## 12. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-18 | Initial GDD created | Claude & User |

---

**Document Status:** APPROVED FOR DEVELOPMENT
**Next Review:** After Milestone 1 completion
