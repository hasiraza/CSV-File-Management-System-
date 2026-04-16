# CSV File Agent 🤖

A modular, agent-based pipeline system for automated CSV processing.

---

#  System Overview

This project follows a **7-step pipeline architecture**:

1. Generate CSV
2. Organize files
3. Clean data
4. Process records
5. Update values
6. Verify results
7. Summarize output

---

#  Agent Architecture

##  Core System

* **[Agent Identity](.agents.md)** → Rules, behavior, and pipeline overview
* **[Planner Agent](agents/planner.md)** → Controls execution flow
* **[Worker Agents](agents/workers.md)** → Perform all tasks

---

##  Worker Responsibilities

| Agent     | Role                |
| --------- | ------------------- |
| Generator | Create CSV files    |
| Organizer | Sort files          |
| Cleanup   | Remove invalid data |
| Processor | Transform data      |
| Updater   | Modify records      |
| Verifier  | Validate output     |

---

#  Skills System

Reusable modules used across agents:

* **[CSV Processor](skills/csv_processor/SKILL.md)**
  → Create, read, update CSV files

* **[File Writer](skills/file_writer/SKILL.md)**
  → Folder creation, file movement

* **[Search](skills/search/SKILL.md)**
  → Fault-tolerant file lookup

* **[Summarizer](skills/summarize/SKILL.md)**
  → Reporting + memory saving

---

#  Data Layer

* **[Architecture](data/documentation/architecture.md)**
  → Full pipeline design

* **Knowledge Base**
  → Python (`csv`, `os`, `shutil`) cheatsheets

* **Memories**
  → Logs + `last_run.json`

---

#  Pipeline Execution

### Run system

```bash
python src/pipeline.py
```

### Run tests

```bash
python -m unittest discover tests
```

---

#  Testing

* **[Test Pipeline](tests/test_pipeline.py)**
* **[Scenarios](tests/scenarios/README.md)**

Includes:

* Happy path
* Missing file
* Error handling
* Edge cases

---

#  Configuration

Environment file:

```
.env
```

Controls:

* Output folder
* Range
* Logging level

---

#  Output

Generated files stored in:

```
/Output/
```

---

#  Full Flow (Simplified)

Planner → Workers → Skills → Output → Summary

---

#  Notes

* Each module is independently testable
* System is fault-tolerant
* Designed for scalability

---

#  Deep Dive (All Docs)

| Section      | Link                                                  |
| ------------ | ----------------------------------------------------- |
| Agent System | [.agents.md](.agents.md)                              |
| Planner      | [agents/planner.md](agents/planner.md)                |
| Workers      | [agents/workers.md](agents/workers.md)                |
| Architecture | [architecture.md](data/documentation/architecture.md) |
| Skills       | [skills/](skills/)                                    |

---

# 🏁Conclusion

This project demonstrates a **clean agent-based architecture** with modular design, reusable components, and structured execution.
