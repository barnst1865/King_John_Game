# King John 1205: Project Roadmap and Schedule

**Version:** 1.0
**Date:** January 18, 2026
**Project Start:** TBD
**Target Completion:** 15-17 weeks from start

---

## 1. Project Overview

### 1.1 Development Philosophy

**Build → Test → Iterate**
- Complete functional systems before moving forward
- Test each milestone before proceeding
- Iterate based on feedback
- Maintain working builds at all times

**Development Approach:**
- Option 2: Build in larger chunks, show for testing at milestones
- User tests and provides feedback
- Emphasis on complete, polished systems over rapid iteration

### 1.2 Success Criteria

**Milestone Success = All criteria met:**
- ✅ All planned features implemented
- ✅ No game-breaking bugs
- ✅ User testing completed
- ✅ Documentation updated
- ✅ Code committed and pushed to git branch

---

## 2. Phase Breakdown

### Phase 1: Core Systems (Weeks 1-3)
**Goal:** Establish foundation - game loop, resources, UI, save/load

### Phase 2: Event Engine (Weeks 4-5)
**Goal:** Complete event system capable of handling all event types

### Phase 3: Initial Content & Prototype (Weeks 6-7)
**Goal:** Vertical slice - playable segment demonstrating all systems

### Phase 4: Content Expansion (Weeks 8-12)
**Goal:** Create all events, chains, and narrative content

### Phase 5: Polish & Features (Weeks 13-15)
**Goal:** Add quality-of-life features, enhance UI, balance

### Phase 6: Testing & Release Prep (Weeks 16-17)
**Goal:** Full playthroughs, bug fixes, final polish

---

## 3. Detailed Phase Plans

## Phase 1: Core Systems (Weeks 1-3)

### Week 1: Foundation

**Tasks:**
1. **Project Setup**
   - Initialize git repository structure
   - Create file/folder organization
   - Set up Python environment
   - Create basic README

2. **Date/Calendar System**
   - Implement `Date` class
   - Day incrementing
   - Feast day tracking
   - Medieval calendar calculations
   - Day of week calculations

3. **Location/Travel System**
   - Create location data structure
   - Travel distance calculations
   - Simple travel mechanics

**Deliverables:**
- Working date system (can advance through year)
- Location system functional
- Basic file structure in place

**Testing:**
- Unit tests for Date class
- Verify date advancement (including month/year rollovers)
- Verify feast day detection

---

### Week 2: Game State & Resources

**Tasks:**
1. **GameState Class**
   - Implement complete GameState class
   - All 18 trackable values (4 core + 8 barons + 6 regions)
   - Consequence application system
   - Derived metrics (averages, calculations)
   - Game over checking

2. **Resource Management**
   - Resource change calculations
   - Clamping (keep values in valid ranges)
   - Resource interaction effects

3. **Save/Load System**
   - Save Manager implementation
   - JSON serialization/deserialization
   - Multiple save slots
   - Auto-save functionality
   - Save file validation

**Deliverables:**
- Complete GameState class
- Functional save/load system
- Resource system operational

**Testing:**
- Unit tests for GameState methods
- Save/load round-trip testing
- Resource change calculations accurate
- Game over conditions trigger correctly

---

### Week 3: UI and Game Loop

**Tasks:**
1. **UI System**
   - Terminal display functions
   - Resource dashboard
   - Color support (optional colorama)
   - Text formatting and wrapping
   - Input handling
   - Clear screen / display functions

2. **Main Game Loop**
   - Basic game loop structure (4 phases per day)
   - Main menu system
   - Save/load/continue menu
   - Day advancement logic
   - Game over handling

3. **Milestone 1: Complete Day Cycle**
   - One complete day with all 4 phases
   - Placeholder event for testing
   - Resources update correctly
   - Save/load works mid-game

**Deliverables:**
- Functional UI system
- Working main game loop
- **Milestone 1 complete: One full day cycle playable**

**Testing:**
- Day cycle completes without errors
- UI displays correctly on different terminals
- Save/load preserves state accurately
- Resources display and update correctly

**User Testing:**
- User plays through one day cycle
- Feedback on UI clarity and usability
- Identify any confusing elements

---

## Phase 2: Event Engine (Weeks 4-5)

### Week 4: Event Classes and Manager

**Tasks:**
1. **Event Classes**
   - Implement `Event` class
   - Implement `Choice` class
   - Implement `EventChain` class
   - Condition checking logic
   - Requirement validation

2. **Event Manager**
   - EventManager class
   - Event loading system
   - Event selection algorithm (priority queue)
   - Triggered event tracking
   - Random event selection

3. **Consequence Engine**
   - Apply consequences to game state
   - Resource change calculations
   - Flag setting/checking
   - Cascading effects

**Deliverables:**
- Complete event class hierarchy
- Functional EventManager
- Consequence system working

**Testing:**
- Event conditions evaluate correctly
- Event selection prioritizes appropriately
- Consequences apply accurately
- No duplicate event triggering

---

### Week 5: Event Processing and Presentation

**Tasks:**
1. **Event Presentation**
   - Event display UI
   - Choice listing
   - Historical context display
   - Advisor consultation integration (basic)

2. **Event Resolution**
   - Process chosen actions
   - Display outcomes
   - Show resource changes with color
   - Record to event history

3. **Event Templates**
   - Template instantiation system
   - Variable replacement (names, locations, etc.)
   - Random parameter generation

4. **Multi-Day Chains**
   - Chain progression logic
   - Chain state tracking
   - Chain event scheduling

**Deliverables:**
- Complete event presentation system
- Event resolution working
- Templates and chains functional

**Testing:**
- Events display correctly
- All choice types work
- Resource changes show clearly
- Chains progress correctly across days

---

## Phase 3: Initial Content & Prototype (Weeks 6-7)

### Week 6: Sample Content Creation

**Tasks:**
1. **Historical Events (15 events)**
   - Pentecost Invasion (June 5)
   - Death of Archbishop Hubert Walter (July 13)
   - Christmas Court (December 25)
   - 12 other major historical moments

2. **Event Templates (5 templates)**
   - Petitioner requests charter
   - Intelligence report
   - Social occasion
   - Religious request
   - Administrative matter

3. **Random Events (5 events)**
   - Unexpected opportunities
   - Minor crises
   - Flavor events

4. **Multi-Day Chain (1-2 chains)**
   - Pentecost Invasion Crisis (June 1-10)
   - Archbishop Succession (July-August)

**Deliverables:**
- 15 historical events written and implemented
- 5 event templates functional
- 5 random events
- 1-2 multi-day chains
- All events tested individually

**Testing:**
- Each event can be triggered
- All choices work
- Consequences apply correctly
- Chains progress smoothly

---

### Week 7: Vertical Slice Integration & Testing

**Tasks:**
1. **Advisor System (Basic)**
   - Implement 5 advisors
   - Basic advice generation
   - Consultation UI

2. **Journal/History System**
   - Event record storage
   - Journal display UI
   - Search/filter (basic)

3. **Integration**
   - Integrate all Phase 1-3 systems
   - Connect events to game loop
   - Balance initial resource values
   - Polish UI for vertical slice

4. **Milestone 2: Vertical Slice Complete**
   - Can play through multiple days
   - Multiple event types trigger
   - Advisors provide input
   - Journal tracks history
   - Save/load works throughout

**Deliverables:**
- **Milestone 2 complete: Vertical slice playable**
- Advisor system functional
- Journal system working
- All systems integrated

**Testing:**
- Full playthrough of vertical slice (2-3 weeks in-game)
- Test all event types
- Verify system integration
- Balance check (resources too easy/hard to manage?)

**User Testing (Major Milestone):**
- User plays vertical slice (30-60 minutes)
- Provide detailed feedback:
  - Is it fun/engaging?
  - Is the UI clear?
  - Are choices meaningful?
  - What's confusing?
  - What needs improvement?
- Iterate based on feedback before Phase 4

---

## Phase 4: Content Expansion (Weeks 8-12)

### Week 8-9: Historical Events Completion

**Tasks:**
1. **Historical Events (remaining 45 events)**
   - Research and write all remaining events
   - Implement in code/JSON
   - Test each event individually
   - Balance resource consequences

2. **Event Quality Pass**
   - Proofread all text
   - Verify historical accuracy
   - Add historical context notes
   - Ensure consistent tone/style

**Deliverables:**
- All 60 historical events complete
- Historical accuracy verified
- All events tested

**Testing:**
- Spot-check random events
- Full year playthrough to verify event flow
- Historical accuracy review

---

### Week 10: Templates, Random Events, and Chains

**Tasks:**
1. **Event Templates (remaining 25)**
   - Create all 30 templates
   - Test instantiation system
   - Ensure variety in generated events

2. **Random Events (remaining 45)**
   - Write all 50 random events
   - Balance probability/impact
   - Test triggering conditions

3. **Multi-Day Chains (remaining 18-19)**
   - Create all 20 chains
   - Test progression logic
   - Verify narrative flow

**Deliverables:**
- All templates complete (30 total)
- All random events complete (50 total)
- All chains complete (20 total)

**Testing:**
- Template generation creates coherent events
- Random events trigger at appropriate frequency
- Chains don't conflict with each other
- All chain branches work

---

### Week 11: Triggered Events and Content Balance

**Tasks:**
1. **Triggered Events (40 events)**
   - Create all condition-based events
   - Test triggering logic
   - Ensure no duplicate triggers

2. **Content Balance Pass**
   - Review all resource consequences
   - Adjust for game balance
   - Ensure no dominant strategies
   - Verify difficulty curve

3. **Character Development**
   - Flesh out advisor personalities
   - Write varied advisor dialogue
   - Implement relationship-based responses

**Deliverables:**
- All 40 triggered events complete
- Content balanced
- Advisor system enhanced

**Testing:**
- Triggered events fire at correct times
- Multiple playthroughs to test balance
- Different strategies are viable
- No trivial "winning" path

---

### Week 12: Narrative Branching and Alternate Paths

**Tasks:**
1. **Branch Testing**
   - Test all major narrative branches
   - Invasion success path
   - Invasion failure path
   - Archbishop succession variations
   - De Braose loyalty/fall variations

2. **Alternate Events**
   - Create alternate versions for divergent timelines
   - Ensure branches don't dead-end
   - Test branch convergence points

3. **Flag System Audit**
   - Document all flags and their effects
   - Test flag logic
   - Ensure no orphaned flags

4. **Milestone 3: Content Complete**
   - Full year playable with all content
   - All branches tested
   - Content polished

**Deliverables:**
- **Milestone 3 complete: Full game content done**
- All narrative branches working
- Flag system robust

**Testing:**
- Multiple full playthroughs (different paths)
- Test extreme resource scenarios
- Verify all endings reachable

**User Testing (Major Milestone):**
- User plays full year (or significant portion)
- Test major decision branches
- Feedback on pacing, balance, engagement
- Note any confusing narrative elements

---

## Phase 5: Polish & Features (Weeks 13-15)

### Week 13: UI Enhancement

**Tasks:**
1. **Enhanced Dashboard**
   - Detailed resource view
   - Baron relationship details
   - Regional stability breakdown
   - Visual bars/indicators

2. **Journal Enhancements**
   - Search functionality
   - Filter by event type
   - Statistics view
   - Export journal to text file

3. **Advisor Panel**
   - Improved consultation UI
   - Advisor relationship display
   - Advice history

4. **Visual Polish**
   - ASCII art elements (optional)
   - Improved text formatting
   - Better color scheme
   - Layout refinements

**Deliverables:**
- Enhanced UI system
- Improved journal
- Better information display

**Testing:**
- UI clarity and readability
- All new features functional
- Performance (no lag)

---

### Week 14: Achievement and Ending System

**Tasks:**
1. **Achievement System**
   - Implement achievement tracking
   - Create 15-20 achievements
   - Achievement display UI
   - Achievement notifications

2. **Ending System**
   - Multiple ending scenarios
   - End-of-year scoring calculation
   - Historical comparison report
   - Alternate history summary
   - Final grade/title assignment

3. **Replay Features**
   - New Game+ options (optional)
   - Historical accuracy challenge mode
   - Starting scenario variations

**Deliverables:**
- Achievement system complete
- Multiple endings implemented
- End-of-year report polished

**Testing:**
- All achievements can be unlocked
- Endings trigger correctly
- Scoring calculation accurate
- End-year report is satisfying

---

### Week 15: Balance and Quality of Life

**Tasks:**
1. **Final Balance Pass**
   - Adjust resource gain/loss rates
   - Fine-tune difficulty
   - Ensure viable multiple strategies
   - Remove exploits

2. **Quality of Life Features**
   - Skip/fast-forward quiet days
   - Quick-save hotkey
   - Settings menu (color on/off, etc.)
   - Tooltips and help text
   - Tutorial/intro improvements

3. **Performance Optimization**
   - Optimize slow functions
   - Reduce memory usage
   - Faster load times

4. **Milestone 4: Polish Complete**
   - All features implemented
   - UI polished
   - Balance finalized
   - Performance optimized

**Deliverables:**
- **Milestone 4 complete: Feature-complete build**
- Game balanced
- QOL features added
- Performance optimized

**Testing:**
- Multiple playthroughs for balance
- Test all QOL features
- Performance benchmarking

**User Testing:**
- User plays complete game
- Focus on overall experience
- Final feedback before release candidate

---

## Phase 6: Testing & Release Prep (Weeks 16-17)

### Week 16: Comprehensive Testing

**Tasks:**
1. **Full Playthroughs**
   - Complete at least 3 full playthroughs
   - Test different strategies
   - Test all major branches
   - Document any issues

2. **Bug Fixing**
   - Fix all critical bugs
   - Fix high-priority bugs
   - Document minor/cosmetic bugs for future

3. **Edge Case Testing**
   - Extreme resource values (0, 100)
   - Unusual player decisions
   - Save/load at critical moments
   - Rapid input/stress testing

4. **Text Proofreading**
   - Comprehensive proofread of all text
   - Fix typos
   - Ensure consistent style
   - Check historical accuracy

**Deliverables:**
- All critical bugs fixed
- All text proofread
- Edge cases handled

**Testing:**
- Systematic testing checklist
- Cross-platform testing (Windows, Mac, Linux)
- Different terminal sizes
- Save file corruption testing

---

### Week 17: Release Candidate and Documentation

**Tasks:**
1. **Release Candidate Build**
   - Create RC build
   - Final testing
   - Version numbering

2. **Documentation**
   - Player-facing README
   - Installation instructions
   - How to play guide
   - Known issues list
   - Credits

3. **Packaging**
   - Create standalone executable (PyInstaller)
   - Test distribution
   - Create release package

4. **Final Review**
   - Team review of complete game
   - Last-minute polish
   - Prepare release announcement

**Deliverables:**
- **Release Candidate v1.0**
- Complete documentation
- Distribution package ready

**Final User Testing:**
- User plays release candidate
- Final approval
- Any last-minute critical issues addressed

---

## 4. Milestone Summary

| Milestone | Week | Description | Success Criteria |
|-----------|------|-------------|------------------|
| **M1** | 3 | Core Loop | One complete day cycle functional |
| **M2** | 7 | Vertical Slice | 10-15 events playable, all systems integrated |
| **M3** | 12 | Content Complete | Full year playable with all content |
| **M4** | 15 | Polish Complete | All features done, balanced, polished |
| **RC** | 17 | Release Candidate | Shippable product, documented |

---

## 5. Risk Management

### 5.1 Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Content creation takes longer than expected | Medium | High | Start content early, prioritize historical events, use templates |
| Balance issues hard to fix late | Medium | Medium | Regular playtesting, balance focus in Weeks 11-15 |
| Scope creep | Medium | Medium | Strict adherence to GDD, defer "nice-to-have" features |
| Performance issues | Low | Medium | Optimize early, profile code, keep design simple |
| User feedback requires major changes | Low | High | Early user testing at M2, allow time for iteration |
| Save file corruption | Low | High | Robust validation, backup saves, thorough testing |

### 5.2 Contingency Plans

**If falling behind schedule:**
1. Reduce number of random events/templates (can add later)
2. Simplify UI polish (focus on functionality)
3. Defer achievement system to post-launch
4. Reduce number of multi-day chains (focus on quality over quantity)

**If major user feedback requires changes:**
1. Allocate Week 8 for revisions if needed after M2 testing
2. Adjust Phase 4 schedule to accommodate
3. Prioritize gameplay-critical changes over polish

---

## 6. Development Workflow

### 6.1 Daily Workflow

**Development Days:**
1. Review current task from phase plan
2. Implement feature/content
3. Write unit tests (if applicable)
4. Local testing
5. Commit to git with clear message
6. Update progress notes

**Milestone Days:**
1. Complete all milestone tasks
2. Comprehensive testing
3. Create build for user testing
4. Documentation update
5. User testing session
6. Collect feedback
7. Plan iteration if needed

### 6.2 Git Workflow

**Branch Strategy:**
- `claude/king-john-adventure-game-cEQCi` - main development branch
- Commit frequently with descriptive messages
- Push at end of each work session

**Commit Message Format:**
```
[Phase X] Brief description

- Detailed change 1
- Detailed change 2
- Testing notes
```

**Example:**
```
[Phase 1, Week 2] Implement GameState class and save system

- Created GameState class with all 18 tracked values
- Implemented consequence application logic
- Added SaveManager with JSON serialization
- Unit tests for save/load round-trip
- Tested with various game states
```

### 6.3 Testing Workflow

**Unit Testing (ongoing):**
- Write tests for core systems
- Run test suite before commits
- Maintain test coverage

**Integration Testing (weekly):**
- Test interactions between systems
- Verify data flow
- Check for conflicts

**User Testing (at milestones):**
- Prepare test build
- Create testing checklist/questions
- Observe user playing (if possible)
- Collect structured feedback
- Prioritize feedback for action

---

## 7. Communication and Documentation

### 7.1 Progress Tracking

**Weekly Updates:**
- Summary of completed tasks
- Current status vs. plan
- Blockers or concerns
- Preview of next week's work

**Milestone Reports:**
- Milestone completion status
- User testing results
- Key learnings
- Adjustments to plan if needed

### 7.2 Decision Log

Major design decisions should be documented:

| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| 2026-01-18 | Use multi-phase daily structure | Provides varied gameplay, breaks up monotony | Increases UI complexity |
| TBD | ... | ... | ... |

### 7.3 Living Documents

These documents should be updated throughout development:
- `CHANGELOG.md` - Track all changes
- `TODO.md` - Active task list
- `BUGS.md` - Known issues
- Design docs updated when design changes

---

## 8. Post-Release Plan

### 8.1 Version 1.0 Release

**Launch Checklist:**
- [ ] All critical bugs fixed
- [ ] Full game playable start to finish
- [ ] Documentation complete
- [ ] Multiple platform testing done
- [ ] Save system robust
- [ ] User-tested and approved

### 8.2 Post-Launch Support (Optional)

**Version 1.1 (Weeks 18-20):**
- Bug fixes from player reports
- Balance adjustments based on feedback
- Quality-of-life improvements
- Minor content additions

**Version 1.2+ (Future):**
- New event packs
- Additional years (1206, 1207...)
- Web version port
- Modding support

### 8.3 Success Metrics

**Development Success:**
- Complete on time (or within 1-2 weeks)
- All major features implemented
- High quality, low bug count
- Positive user feedback

**Gameplay Success:**
- Playable and engaging full year
- Multiple viable strategies
- Replayability (different paths)
- Educational and entertaining

---

## 9. Resource Requirements

### 9.1 Time Commitment

**Per Week:**
- Development time: Variable (as available)
- Option 2 approach: Larger chunks, less frequent check-ins
- User testing: 1-2 hours per milestone

**Total Project:**
- 15-17 weeks
- User involvement: 5-6 testing sessions (1-2 hours each)

### 9.2 Tools and Infrastructure

**Development:**
- Python 3.9+
- Git / GitHub
- Text editor / IDE
- Terminal emulator

**Testing:**
- Multiple OS access (Windows, Mac, Linux) preferred
- Various terminal emulators

**Distribution:**
- GitHub for code hosting
- GitHub Releases for distribution
- Optional: Website for project page

---

## 10. Gantt Chart

```
Week | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
-----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----
Setup| ██ |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
Date | ██ |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
State|    | ██ |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
UI   |    |    | ██ |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
Event|    |    |    | ██ | ██ |    |    |    |    |    |    |    |    |    |    |    |    |
Conte|    |    |    |    |    | ██ | ██ | ██ | ██ | ██ | ██ | ██ |    |    |    |    |    |
Polis|    |    |    |    |    |    |    |    |    |    |    |    | ██ | ██ | ██ |    |    |
Test |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | ██ | ██ |
-----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----
M1   |    |    | ✓  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
M2   |    |    |    |    |    |    | ✓  |    |    |    |    |    |    |    |    |    |    |
M3   |    |    |    |    |    |    |    |    |    |    |    | ✓  |    |    |    |    |    |
M4   |    |    |    |    |    |    |    |    |    |    |    |    |    |    | ✓  |    |    |
RC   |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | ✓  |
```

---

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-18 | Initial roadmap created | Claude & User |

---

**Document Status:** APPROVED
**Next Review:** After Milestone 1 completion (Week 3)
