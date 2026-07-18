# Neverlost Private Judge Repository Handoff

**As-of date:** 2026-07-17  
**Operating timezone:** America/Denver  
**Status:** `PRIVATE_REPOSITORY_PACKAGE_READY_FOR_REMOTE_CREATION`

## Repository settings

- **Recommended repository name:** `neverlost-build-week`
- **Visibility:** Private
- **Description:** Governed, capacity-aware Codex workflow for turning scattered human reality into evidence-aligned action.
- **Initialize remote with README:** No; the local repository already contains the controlling history.
- **Public license:** None selected; the private repository is supplied for contest judging and testing.
- **Required access period:** Keep the repository and test path available through August 5, 2026 at 5:00 p.m. Pacific Time.

## Required judge access

After the private remote exists, invite both official testing addresses:

- `testing@devpost.com`
- `build-week-event@openai.com`

Do not place the Codex Session ID, account credentials, personal appointment information, or other private submission values inside the repository.

## GitHub website path

1. Create a new **private** repository named `neverlost-build-week`.
2. Leave README, `.gitignore`, and license initialization unchecked.
3. Copy the repository's Git URL.
4. Push the existing local `main` branch.
5. Open **Settings → Collaborators** for the private repository.
6. Invite both official testing addresses above.
7. Confirm both invitations were issued and preserve evidence of the access configuration.

## Local push commands

Replace `<PRIVATE_REPOSITORY_GIT_URL>` with the Git URL shown by GitHub:

```bash
git remote add origin <PRIVATE_REPOSITORY_GIT_URL>
git push -u origin main
```

If an `origin` remote already exists, inspect it before changing anything:

```bash
git remote -v
```

Do not overwrite an unexpected remote without review.

## Post-push repository patch

Replace every `<PRIVATE_REPOSITORY_URL>` placeholder in `README.md` and `docs/PLUGIN_INSTALLATION.md` with the judge-accessible repository URL, commit the change, and push it.

## Remote acceptance test

Use an account with repository access to clone into a fresh directory, then run:

```bash
python3 scripts/run_stage4_demo.py
python3 scripts/validate_stage4_package.py
python3 scripts/smoke_test.py
python3 -m unittest discover -s tests -v
```

Pass condition:

- demo status matches the README;
- package validation is 17 of 17;
- all six unit tests pass;
- no private submission value appears in tracked files; and
- both official judge addresses retain access.

## Devpost fields retained separately

- Private repository URL
- Codex `/feedback` Session ID
- Public YouTube URL
- Final text description
- Testing instructions
- Submission receipt

