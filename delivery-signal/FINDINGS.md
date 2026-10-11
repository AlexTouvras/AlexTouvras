# Trial on public work-item files

Run on 11 Oct 2026 with the same checker the configuration page uses. The files stayed on this machine. No tracker token was used. Approval stayed pending. These are public files, not a customer delivery.

## What was run

| File | Source | Rows | Shape |
| --- | --- | --- | --- |
| Jira Cloud export | [rodecarv/Jira-To-CodeArts-Req `jira.csv`](https://github.com/rodecarv/Jira-To-CodeArts-Req/blob/main/jira.csv) | 2 | Issue key, Summary, Status, Due date, `Custom field (Story point estimate)`, `Custom field (Target end)` |
| Tutorial Jira sheet | [fearfactor3/jupyter-notebooks `sample_jira_issues.csv`](https://github.com/fearfactor3/jupyter-notebooks) | 3 | `Issue Key`, Summary, Status, Priority, Assignee, `Due Date` |
| phpBB Jira export | [avocadosmash/phpbb-lab `setup/exported-issues.csv`](https://github.com/avocadosmash/phpbb-lab/blob/main/setup/exported-issues.csv) | 481 | Full Jira header, two projects, priorities Blocker / Major / Minor / Trivial |
| Azure DevOps example | The five-row export printed on [Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/boards/queries/import-work-items-from-csv) | 5 | ID, Work Item Type, Title, Assigned To, State, Tags |
| Same example with the extra columns that page describes | Priority, Changed Date, Due Date, and `Name <email>` assignees added to that shape | 5 | Azure DevOps |
| Renamed headers | Column names from a third-party importer (`Id`, `Type`, `Title`, `State`, `AssignedTo`) | 3 | Not a known export |

Each file was built twice where the dates were old: once as of 11 Oct 2026, and once as of the week of the newest update in the file.

## 1. Configuration is seamless only for the two header shapes we already named

A normal Jira export and a normal Azure DevOps export were accepted with no mapping file. `Issue Key` and `Due Date` matched `Issue key` and `Due date`. Jira dates such as `09/Jan/24 3:54 PM` were read. Azure DevOps priority `1` and `2` became Highest and High, and `Name <email>` was stripped to the name. The richer Microsoft-shaped file produced two questions, including who owns work item 273.

The renamed file was refused. The message named the headers it saw and the three shapes it knows. That is a clear stop, and the repair is `columns.json`. The configuration page has no upload for that file and no way to point at a column. A person who hits this stop has to leave the page and edit JSON.

Other seams:

- The connected project key is not used when the CSV has no project column. The Microsoft example and the tutorial sheet were both reported as a project named Portfolio, with a data-quality line per row. That line is in the Markdown file and not on the HTML the page shows.
- A file with two projects (phpBB and Website) is reported as two pulses. The page cannot limit the brief to one of them.
- The report date defaults to today. For a 2024 export that makes every real due date late. For these files it barely mattered, because the rules that would notice a late date did not fire.
- After a file is chosen, the page does not say which columns it used. `Custom field (Story point estimate)` and `Custom field (Target end)` were present on the small Jira file and were not read. phpBB's `Custom field (Story Points)`, `Due Date`, and `Custom field (Target end)` headers were present and every cell was empty, so a mapping would not have added dates or points.

## 2. The brief is actionable on a small, familiar export, and it gives a false green on a real tracker

The two-row Jira file produced one cited question: who owns PT-1. The summary in the file is `summary1`, so the question cannot be more specific than the export. That path works.

The five-row Microsoft example, with no priority and no dates, produced no risks and said the portfolio is on track. Adding priority, a changed date, and a due date changed the same shape into two cited questions. The difference is the columns, and the page does not ask for them.

The phpBB export is the serious test. 481 work items, updated from 2015 through 5 Nov 2025. Nine items are priority Blocker, and eight of those have no assignee. Examples still open on 5 Nov 2025 include PHPBB-17561 and PHPBB-17550. The brief, both as of 5 Nov 2025 and as of 11 Oct 2026, said:

> As of 11 Oct 2026, 2 of 2 projects are on track (phpBB, Website).

Result `e83da54456`. Zero risks, zero questions. The reasons:

- Priority names Blocker, Major, Minor, and Trivial are kept as written. The unassigned rule only fires for Highest and High. Major is 149 items. Blocker is 9. None of them count.
- Due dates and target ends are empty, so nothing is overdue.
- Statuses `Patch Awaiting Review` (40), `Confirmed` (4), `Awaiting Information` (3), and `Patch Needs Work` (1) are not treated as in progress, waiting, or blocked. The HTML does not show that list. The Markdown data-quality section does.
- Stale work is only raised when a notes file says the project is on track. A raw CSV has no notes file, so a year without an update never becomes a finding.
- Story point cells were empty, so the epic-completion rule had nothing to compare.

The tutorial sheet has the same shape of miss. One item is `In Review`. All three have assignees. As of 11 Oct 2026 they are past their due dates. The brief says the portfolio is on track, result `cceee6bf58`.

That result id is also the id of the five-row Microsoft example. The id is a hash of the findings, the set-aside list, the decisions, the pulse, and the change list. When nothing fires and the only pulse is `Portfolio` / on track, different files share one id. It still means "the rules produced this reading." It does not mean "this is the same export."

So the end result is efficient when the columns and the words match the sample, and it is the wrong instruction when they do not: it tells a reader the tracker is healthy.

## 3. What to ship next, in this order

1. Do not call a project on track when no rule could run. If the file has open items and zero findings, the first screen should say what was missing: unrecognized priorities, unrecognized statuses, no due dates, no story points. Put that on the HTML, not only in the Markdown.
2. Treat Jira's Blocker as Highest and Major as High. On the phpBB file that would have asked who owns the unassigned blockers. Rank Blocker above Major so five similar cards do not hide the blockers.
3. When many rows share one pattern, say the count. "8 blockers have no assignee" is the action. Five separate cards with the same sentence is not.
4. Raise stale and overdue items without a notes file. The notes rule is right for a pack that includes notes. A CSV alone never has that file, and that was every public export here.
5. Add default aliases for `Custom field (Story point estimate)`, `Custom field (Target end)`, and `Custom field (Epic Link)` when Due date, story points, or Parent are empty.
6. A second week is still untested on real data. None of these files had a previous export. The change list remains the reason to come back, and it needs one team with two weeks.

A customer file is still the right next input. These public files are enough to stop shipping a false green, and not enough to add a fourth tracker.

## 4. Options to add on the configuration page

After the CSV is chosen, show a short reading of the file before the report:

- Columns that were used, and columns that look like a due date, story points, or a parent and were not used. Let the person pick the column on the page instead of writing `columns.json`.
- The priority words in the file, with Blocker and Major already marked as high, and a way to change that.
- The status words that were not recognized, with a way to mark them in progress, waiting, or done.
- If the file has more than one project key, a choice of one project or all of them.
- If the file has no project column, use the project key already typed on the page.
- If the newest Updated date is far from today, show that date next to the report date so a 2024 export is not read as this week by accident.
- If the report has no risks, show the data-quality lines on the page. The current page shows the HTML brief, and that HTML omits them.

The token field, the site, and the project key can stay as they are. The gap is the file, not the connection.
