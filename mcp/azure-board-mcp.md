---
name: azure-board-mcp
description: Interact with Azure DevOps — work items, tasks, bugs, sprints, backlogs, pull requests, repositories, builds, and pipelines. Use when the user asks about ADO, Azure Boards, their tasks, sprint, backlog, a PR, build status, or anything in their Azure DevOps project.
---

# Azure DevOps (azure-board-mcp)

## Setup
If no project is active, call `switch_project` first — it lists all projects and remembers the choice.

## Tool quick-reference

| User asks | Call |
|---|---|
| My tasks / what should I work on | `list_work_items` mine=true |
| Current sprint / sprint board | `list_work_items` sprint=true |
| Specific ticket #123 | `get_work_item` id=123 |
| All active bugs / stories / epics | `list_work_items` type + state filters |
| Create a task / bug / story | `create_work_item` |
| Close / reassign / update a ticket | `update_work_item` |
| Comment on a ticket | `add_comment` |
| Link two tickets (parent, related) | `link_work_items` |
| Advanced query | `query_wiql` |
| Ordered product backlog | `get_backlog` |
| Who changed a ticket / audit trail | `get_work_item_history` id=123 |
| Valid area / iteration path values | `list_paths` kind="area" or "iteration" |
| Who's on the team | `list_team_members` |
| Kanban columns / board layout | `get_board` |
| Repos in the project | `list_repos` |
| Browse files | `list_files` → `get_file` |
| Recent commits | `list_commits` |
| Open PRs / reviewer status | `list_pull_requests` |
| Open a pull request | `create_pr` |
| Build status / CI health | `list_builds` |
| Why did a build fail | `get_build_timeline` (which step) → `get_build_logs` (output) |
| Stop a running build | `cancel_build` |
| Trigger a pipeline | `list_pipelines` → `run_pipeline` |
| Releases / deploy status | `list_releases`, `create_release` |
| Sprint dates / team capacity | `get_sprint` |

## Rules
- Never ask the user to type a project name — use `switch_project` (no args) to list, then switch.
- On 401 errors → call `auth_status` first.
- For list results prefer compact summaries; only call `get_work_item` when full detail is needed.
- Lists are paginated (default page 15, max 50) and report "Showing X–Y of N". To see more, call again with `skip` set to the last index shown — don't ask for a huge `top`.
- Before setting `areaPath`/`iterationPath` on create/update, get exact values from `list_paths`.
