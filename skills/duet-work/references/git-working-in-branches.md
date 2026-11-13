# Working in ticket branches

Read this before any git work in a product repository: a commit, a ticket branch, a rebase, a squash, a push, or shelving or closing a ticket that has a branch.

Ticket branches exist so that several tasks in one repository can move in parallel without stepping on each other. A branch is short-lived: hand its work to review often, and ideally don't keep work unmerged for longer than a day. Long-running feature development over weeks is a different process that this file doesn't cover. Shelving a ticket can save its work in a long-lived branch, but that is storage, not development: work resumes on a new short-lived branch started from it.

These are the rules of the workflow and of the Duet tools that support it, not a git manual. You choose the commands, flags and ways to check things yourself. That freedom doesn't extend to the decisions below: when to commit, rebase or squash, what to publish, and what happens to the work are settled here or by the user. Where a rule asks for the user's word, it means words the user actually said, heard directly or quoted exactly; a judgment of what the user would want, yours or anyone else's, is not that word.

## When a ticket gets a branch

By default, work goes to `main` in the main clone, `@<alias>.git`. A ticket gets a branch only when it is in `work` and the user asks for one. Being in `work` doesn't call for a branch and doesn't permit creating one on your own.

## Naming the branch

Make up a short English name from what the ticket is for, as its notepad's dashboard states the ticket's purpose, or as its `INDEX.md` does when there is no dashboard; the folder name is only a hint. The name is the full ticket number, an underscore, and Latin letters and digits only, with no hyphens or further underscores: `ABC001_DailyScript`. The server checks the form, not the meaning, which is yours to get right.

While a ticket has a branch, it has one name in every repository: for a second repository, pass the name the ticket already has, and don't change it unless the user asks. Renaming the ticket doesn't rename its branch. Shelving or closing erases the name, so a resumed ticket is named again.

## Creating the worktree

Create a branch only with the Duet tool `add_worktree(ticket, repo, branch)`, one repository per call. It puts the branch in a worktree next to the main clone, `@<alias>.wt-ABC001`, and records the branch in `git-branch-name` and the repository in `git-branch-repos` of the ticket's frontmatter. The branch starts from the repository's entry in `git-parked-branches` when there is one, and otherwise from a fresh `origin/main`. Entries survive resuming and closing, so before you create a worktree, check the ticket's entries and settle a stale one with the user; dropping an entry is described under "Resuming a ticket".

Do all work on the ticket in its worktree. The main clone stays on `main`; never switch it to the ticket branch. `@<alias>.git` always means the main clone, whatever ticket you are on, so take the worktree paths from the answers of the ticket tools or from `orientation(path, ticket="ABC001")` and name the worktree explicitly when you hand work to someone.

Git doesn't carry ignored files into a worktree: virtual environments, `node_modules` and build outputs have to be set up in the worktree itself before you can run its tests.

## Committing and review

When you hand work over for review, commit it to the ticket branch in its worktree, so that the review gets a fixed commit rather than a changing tree. Fixes from a review round are committed when you hand them over for the next round. Stopping for the day or reaching an intermediate step is not a reason to commit.

A commit to `main` needs the user's direct request, with a branch or without one. A request for a commit plan is a request for a written plan, not for a commit.

## Updating the branch

Bring new work from `main` into the branch only by rebasing it onto a fresh `origin/main`, never by merging `main` into it, so that the branch stays the ticket's own commits on top of `main`, which review and the final squash rely on.

## Pushing

Any push — of `main`, of the ticket branch, or of anything else — needs the user's explicit permission in direct words. A hint, approval of the result, a request to squash, or a technical need is not that permission. A branch that was published before still needs permission for a force push after a rebase, and a deleted remote branch needs permission to be pushed again. The one exception is deleting the remote ticket branch in the cleanup after a published squash, described below.

## Squashing into main

Work enters `main` as one squash commit, made when the user asks for it, as the rule on commits to `main` above requires. It holds the accepted work rebased onto a fresh `origin/main`, and it passes the repository's own checks before you create it.

After creating the squash commit locally, stop. The user publishes `main`, or you do it on their explicit word. Until it is published, keep the ticket branch, and its remote branch if there is one: the squash can still be undone and redone, and the branch serves fixes to this piece of work, not the start of the next one. Undoing a commit in unpublished history is ordinary work that needs no permission.

## After the squash is published

Once the user has published `main` or told you to, the cleanup below needs no separate word, and it is not permission for any new push. First make sure the squash commit is in an up-to-date `origin/main`, and that the worktree holds no new work that wasn't accepted. Then delete the remote ticket branch, only if it was ever published, and set the local ticket branch to the published `origin/main` before any new work on it.

## Before shelving or closing

`move_ticket` shelves or closes a ticket with a branch only when the branch is ready in every repository where the ticket has it: the worktree has no uncommitted or untracked changes, and the branch's last commit is contained in a fresh `origin/main`, or, when shelving, in the parked branch named for that repository. The server checks readiness; it never decides what to keep, and never discards, squashes or resets work. Preparing the branch is your job, agreed with the user.

Before shelving or closing a ticket, check its worktrees for new or changed files that git ignores: removing a worktree deletes them, and the server's check doesn't see them.

Once the branch is ready, `move_ticket` removes each worktree and the local ticket branch, erases `git-branch-name` and `git-branch-repos`, and moves the ticket. A published remote ticket branch is outside this cleanup; it stays until it is deleted under the push rules above.

## Shelving a ticket

Decide with the user, then prepare each repository where the ticket has its branch:

- **Discard:** set the ticket branch to `origin/main`.
- **Save:** squash the work into one commit on a parked branch, `ABC001_parked-<meaning>`, whose last part names the saved work in lowercase English words joined by hyphens (`ABC001_parked-retry-policy`), then set the ticket branch to that commit.

Then call `move_ticket(ticket, to="backlog", parked={"<alias>": "ABC001_parked-<meaning>"})`, naming each repository whose work was saved. The server records the parked branches in `git-parked-branches`. An entry there means "the next worktree in this repository starts here"; a repository where the ticket has its branch and that you leave out of `parked` has its entry dropped, because its work was discarded or is already in `main`. Saving doesn't require publishing anything, and gives no permission to push.

## Resuming a ticket

Move the ticket back to `work` first; that alone creates no worktree. When work actually resumes and the user asks for a branch, `add_worktree` starts it from the repository's parked branch. Then decide with the user whether to rebase, amend or do something else: don't replace the saved base with `main` or rebase before that decision.

After resuming a ticket that has a parked branch, create a blocker asking what to do with the old parked branch, as `references/blockers-management.md` describes, because the branch and its entry stay until someone removes them, and the entry decides where the next worktree in that repository starts. To drop an entry once it is no longer wanted, shelve without naming that repository in `parked` when the ticket has its branch there, and otherwise pass `""` for it: `move_ticket(ticket, to="backlog", parked={"<alias>": ""})`, which moves the ticket to the backlog if it isn't there already; on a closed ticket that reopens it and records the date.

## Closing a ticket

Sort out unmerged work before closing: either shelve the ticket, or discard the work and then close it. For closing, readiness means the branch's last commit is in a fresh `origin/main`, which is what the cleanup after a published squash leaves. Closing leaves parked branches and their entries alone; what happens to them is yours to settle with the user. Reopening a ticket doesn't restore its branch.

## When a tool refuses

Tell the user and sort the situation out by hand; there are no recipes for this. An error from `move_ticket` while it removes worktrees names the repository, the worktree path, the branch, the checked commit and what was already done, and the ticket's `git-branch-repos` keeps listing what the server hasn't removed yet. That is enough to put the repository back with git into the state the fields describe and retry the call. An `add_worktree` error has created nothing unless it names what was left on disk without being recorded.
