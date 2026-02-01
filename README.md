# I'm In - Security Research Automation Pipeline

**Mission**: Automate the grunt work, focus on impact.

This project automates vulnerability hunting and content publishing for security research. Two core pipelines working together:

1. **Vulnerability Hunting** - Monitor targets (IoT firmware, automotive, mobile apps), detect changes, flag potential vulnerabilities
2. **Content Pipeline** - Transform raw security analysis into blog posts, tweets, and LinkedIn content

**Goal**: Build a system that turns research into discoverable CVEs and consistent output, accelerating career growth in security research.

---

## Project Structure

```
.
├── STRATEGY.md                    # Mission, vision, 18-month roadmap
├── vulnerability-hunting/         # Automated vuln discovery pipeline
│   └── README.md
├── content-pipeline/              # Analysis → content transformation
│   └── README.md
└── README.md                      # This file
```

---

## Quick Start

### Phase 1 (Current): Foundation (0-3 months)

**Vulnerability Hunting**:
- [ ] Select first target (IoT router / automotive firmware / mobile app)
- [ ] Build monitoring script + cron automation
- [ ] Test for 1 month, filter noise
- [ ] Analyze first candidate vulnerability

**Content Pipeline**:
- [ ] Design blog post template (CVE analysis)
- [ ] Build LLM-based draft generator
- [ ] Test with 3 real analysis notes
- [ ] Expand to Twitter threads + LinkedIn

**First Milestone**: 1 CVE candidate found + 4 blog posts published

---

## Core Values

1. **Automation First** - If it's repeatable, automate it
2. **Signal over Noise** - One CVE beats 100 blog posts
3. **Compound Growth** - Each project accelerates the next
4. **Public by Default** - Share knowledge unless there's a reason not to
5. **Ruthless Prioritization** - Impact over hype

---

## Success Metrics

**Leading (weekly)**:
- Monitoring uptime (target: 95%+)
- Content publish frequency (target: 1/week)
- Draft → publish turnaround (target: <3 days)

**Lagging (quarterly)**:
- CVEs discovered & published
- Blog traffic + engagement
- Social media growth
- Conference invitations / job offers

---

## Roadmap

See [STRATEGY.md](STRATEGY.md) for the full 18-month plan, including:
- Detailed phase breakdown
- 5 limitations + mitigation strategies
- Risk management
- Next actions

---

## License

MIT - Use freely, share improvements.

---

**Status**: Phase 0 (Planning) → Phase 1 (Foundation) kickoff  
**Last Updated**: 2026-02-01
