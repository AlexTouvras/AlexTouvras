# Current task

The public-export trial is in the checker. A file that cannot support the rules is not called on track. Blocker and Major count. The product repository is https://github.com/AlexTouvras/delivery-signal

## Verify

`python3 delivery-signal/tests/test_pipeline.py` exits 0. Northline result id remains `e53f514aa6`. A Blocker export leads with the unassigned count. A file with no priority and no due date is Not checked, on the HTML.

## Done

- Jira Blocker is Highest and Major is High
- Unassigned items of one priority are reported as a count from three upward
- Overdue and stale items are raised without a notes file
- Empty due date, story points, and parent fall through to target end, story point estimate, and epic link
- Install links point at `AlexTouvras/delivery-signal`

# Previous task

A connected Jira or Azure DevOps project is fetched. The configuration page does not ask that customer for a CSV. A CSV remains for another tracker, for `run issues.csv`, and for the phone page.

## Verify

`python3 delivery-signal/tests/test_link.py` exits 0. A Jira save that also posts a CSV builds the brief from the tracker. `run import issues.csv` after `run connect jira` reads the tracker. The Jira form hides the CSV fields. `run issues.csv` still writes a brief.

## Done

- Jira and Azure DevOps configuration and `run import` fetch the project
- The fetch asks for story points, target end, and epic link on Jira, and story points, effort, and target date on Azure DevOps
- A posted or named CSV is ignored once those trackers are connected

# Previous task

Decide whether an agent should assess a file before the brief. Decision, in `delivery-signal/FINDINGS.md`: a fixed pass reads the columns and the words in the file, and that reading chooses the lead. The same file still produces the same result id.

## Verify

The decision is recorded. No rule change in this pass.

## Done

- The phpBB false green is the case the first pass has to lead with
- A writing model stays a reader of the finished brief

# Previous task

Trial of public work-item files, written up in `delivery-signal/FINDINGS.md`. The phpBB Jira export (481 items, 9 blockers) was reported on track with no risks. The configuration page needs a column and vocabulary check before that brief is trusted.

## Verify

The notes cite the public files and the result ids from this checker. No product rule was changed in this pass.

## Done

- Jira Cloud, a tutorial sheet, the phpBB export, the Microsoft Learn Azure DevOps example, and a renamed header were run through `brief_from_csv`
- Findings cover configuration, the brief, the next change, and options for the configuration page

# Previous task

The page offers four install options, Apps, One-liner, npm, and Hackable, for macOS & Linux and for Windows. The one-liner puts the command on the machine and uses Python when it is already there.

## Verify

`python3 delivery-signal/tests/test_command.py` exits 0. `install.sh` writes `delivery-signal` and that command writes a brief. The page switches platform and method, and the Windows one-liner is the PowerShell command.

## Done

- Apps, One-liner, npm, and Hackable on the published page
- `install.sh` and `install.ps1`
- `npm install -g` from this repo runs `delivery-signal`

# Previous task

`run` opens a configuration page on this computer. The person chooses Jira, Azure DevOps, or another tracker, imports a CSV or enters a token for one read, and the report opens on that page. The token stays out of the project file.

## Verify

`python3 delivery-signal/tests/test_link.py` exits 0. The page at `/` is the configuration form. A posted CSV builds the brief. A posted Jira token is absent from `project.json`. `run issues.csv` still writes a brief.

## Done

- `run` and `run connect` open http://127.0.0.1:8767
- The form saves the site and the project key, then shows the brief
- A token typed on the page is used for that read and left out of the project file

# Previous task

In the person's own terminal: connect the folder with `run`, connect a Jira, Azure DevOps, or other project or import a CSV, then `run report`.

## Verify

`python3 delivery-signal/tests/test_link.py` exits 0. A connected project file has no token. `run import` with no file reads Jira or Azure DevOps through the stand-in. `run issues.csv` still writes a brief.

## Done

- `run connect jira|ado|other` stores the site and the project key in `.delivery-signal/project.json`
- `run import issues.csv` copies the export; a second import becomes the previous file
- `run import` with no file reads the connected project; the token stays in the environment
- `run report` writes the brief under `out/`

# Previous task

In the person's own terminal, the command is `run` plus their CSV. Command Prompt: `run issues.csv`. PowerShell: `.\run issues.csv`. bash: `./run issues.csv`.

## Verify

`python3 delivery-signal/tests/test_command.py` exits 0. `./run` writes a brief. The skill tells an agent to use that `run` command and not to install anything.

## Done

- `run`, `run.ps1`, and `run.cmd` are the command in bash, PowerShell, and Command Prompt
- A missing Python prints the page link

# Previous task

One command in the shell the person already has. No separate install.

## Verify

`python3 delivery-signal/tests/test_command.py` exits 0. `delivery-signal/run.sh` writes a brief from one CSV. The PowerShell and cmd scripts call the same checker and do not install a package.

## Done

- `run.sh`, `run.ps1`, and `run.cmd` forward one CSV to the checker
- A missing Python prints the page link
- `skills/delivery-signal/SKILL.md` tells an agent CLI to run that command and not to install anything
- The CSV name and today's date are the defaults

# Previous task

Publish Delivery Signal so a phone or a computer can open it from GitHub and connect a CSV. No account. The export stays on that device.

## Verify

`python3 delivery-signal/tests/test_site.py` exits 0. The published files match the checker. The page loads, the Northline sample result id is `e53f514aa6` for the canonical, Jira, and Azure DevOps copies, and a chosen CSV matches `pipeline.brief_from_csv`.

The page opens from the repo at the HTML preview of `docs/index.html`. https://alextouvras.github.io/AlexTouvras/ is the address once GitHub Pages is serving `docs/`. Creating the Pages site returned HTTP 403.

## Done

- `docs/` page with Home Screen install, a CSV form, share, and download
- The page runs `pipeline.py` in the browser so the result id matches this repo
- `connect.py` page with the sample, the export form, and the terminal commands
- `POST /run` for the form and for curl
- Column profiles for canonical, Jira, and Azure DevOps, plus `columns.json`
- One command for a single CSV
- Executive HTML and a dated file meant to be forwarded
- Plan for why a team would pay, and what waits until a second cycle

## Out of scope

- Accounts, checkout, live Jira or Azure DevOps connections
- A claim that a buyer has agreed to pay

# Previous task

Daycare comparison page for Lipstikkakuja 14, Rekola. Child is 7 weeks old on 6 Oct 2026; target start is November 2027 (about 15 months).

## Verify

Open `daycare/index.html` over HTTP (`python3 -m http.server` inside `daycare/`). Map shows home and a 10 km circle. Press a marker and a list row; both open the same card. English filter leaves the four English programmes plus the lighter English-enrichment centres. Default order starts with Pilke Playschool Pohjantähti.

## Done

- 176 daycares inside 10 km: Helsinki region Service Map for Helsinki and Vantaa, OpenStreetMap plus city pages for Kerava and Tuusula
- Score weights English, toddler-age fit, whether Vantaa can actually offer the place, fee versus the municipal cap, and distance
- Map, pressable card, ranked list, filters, shortlist

## Out of scope

- Live vacancy or an application form
- A routed commute time
- Publishing the page from the profile README

## Studio

Temporary Orbit Studio route `/studio/daycare` is prepared in `governance/orbit-studio/` and committed locally on Orbit branch `cursor/studio-daycare-9c6e`. Push to AlexTouvras/Orbit returned HTTP 403 for cursor[bot]. The live Studio does not show the card until that branch is pushed by someone with write access.

## Verify

`python3 governance/tests/test_catalog.py` exits 0.

`python3 governance/server.py` serves the archive at http://127.0.0.1:8765. Filter by repo and topic, save an edit, and restore the previous version.

## Done

- Public corpus imported into `governance/archive/`
- Public markdown listed as kind `doc`
- Orbit and ravens `.cursor` rules, skills, and automations imported
- Similar docs grouped; leftovers stay kind doc
- Local editor with filters, always-on budget, save, and version restore
- Context-budget skill packaged as a Cursor plugin
- Studio page and snapshot prepared in `governance/orbit-studio/`
- Push to AlexTouvras/Orbit denied (HTTP 403). Live `/studio/directives` is not deployed.
- Local Orbit dev server (`STUDIO_DEV_OPEN=1`) served `/studio` and `/studio/directives`. Filtering to Orbit skills showed the five skill files and the visual-storytelling body. The public home page does not link the archive.

## Out of scope

- Publishing saves back to source repositories
- Writing live Cursor Automations
- Private repositories and Customize user rules
