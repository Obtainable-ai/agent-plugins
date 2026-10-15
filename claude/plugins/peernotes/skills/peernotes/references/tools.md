# Peernotes connector: tool catalog

Base tool names (the actual name may carry a server prefix). Required parameters in **bold**. List tools return up to `pageSize` items (default 20, max 50); check `pageInfo.hasNext` and increment `page`.

## Workspaces

| Tool | Parameters | Returns / use |
|------|------------|---------------|
| `listWorkspaces` | — | All workspaces the user belongs to: ORN, name, description, status, topics |
| `getWorkspace` | **workspaceOrn** | Metadata: name, description, topics, status |
| `getWorkspaceSummary` | **workspaceOrn** | Resource counts and the workspace's AI instructions |

## Search

| Tool | Parameters | Use |
|------|------------|-----|
| `search` | **workspaceOrn**, **query**, resourceTypes (THOUGHT/NOTE/SOURCE), author, updatedAfter, updatedBefore (ISO-8601), page, pageSize | Full-text search across thoughts, notes and sources |

## Notes

| Tool | Parameters | Use |
|------|------------|-----|
| `getOwnedNotes` | **workspaceOrn**, page, pageSize | Notes the user owns |
| `getSharedNotes` | **workspaceOrn**, page, pageSize | Notes shared with the whole workspace |
| `getCollaboratedNotes` | **workspaceOrn**, page, pageSize | Notes where the user is a collaborator |
| `getNote` | **orn** | Full content, linked thoughts, topics, comments |
| `getNoteRevisions` | **noteOrn** | All revisions, oldest (0) first, with title and content |
| `generateNote` | **workspaceOrn**, **thoughtOrns**, sourceOrns, prompt, noteOrn (update), referenceNoteOrn (match format), sharedWithWorkspace | Create or regenerate a note with AI |
| `rewriteNote` | **workspaceOrn**, **noteOrn**, **selectedText** (verbatim, one block), **prompt** | AI-rewrite one section; rest unchanged |
| `revertNote` | **workspaceOrn**, **orn**, **revisionNumber** (0 = oldest) | Restore an earlier revision |
| `deleteNote` | **orn** | Permanent delete (confirm first) |

## Thoughts

| Tool | Parameters | Use |
|------|------------|-----|
| `getThoughts` | **workspaceOrn**, page, pageSize | Thoughts the user owns |
| `getSharedThoughts` | **workspaceOrn**, page, pageSize | Thoughts shared with the workspace |
| `getThought` | **orn** | Content, comments, topics |
| `getThoughtRevisions` | **thoughtOrn** | Revision history |
| `saveThought` | **workspaceOrn**, **content**, sharedWithWorkspace | Create a thought (private unless shared) |
| `deleteThought` | **orn** | Permanent delete (confirm first) |

## Sources

| Tool | Parameters | Use |
|------|------------|-----|
| `getOwnedSources` | **workspaceOrn**, page, pageSize | Sources the user owns |
| `getSharedSources` | **workspaceOrn**, page, pageSize | Sources shared with the workspace |
| `getSource` | **orn** | Content, comments, and `meetingAttributes` / `threadAttributes` / `agentSessionAttributes` for those types |
| `saveMeetingSource` | **workspaceOrn**, **name**, **content** (Markdown transcript), provider (ZOOM/GOOGLE_MEET/MICROSOFT_TEAMS/SLACK_HUDDLE/OTHER), externalId, url, startedAt, endedAt (ISO-8601), attendees [{displayName, email, externalId}], recordingUrl, orn (replace), sharedWithWorkspace | A meeting: transcript as content, everything else as metadata |
| `saveThreadSource` | **workspaceOrn**, **name**, **content** (Markdown messages), provider (SLACK/MICROSOFT_TEAMS/DISCORD/OTHER), externalId, url, teamName, channelId, channelName, participants, linkedFiles, startedAt, endedAt, orn, sharedWithWorkspace | A chat thread |
| `saveAgentSessionSource` | **workspaceOrn**, **name**, **content** (Markdown prompts/responses), provider (CLAUDE_CODE, CLAUDE_COWORK, CODEX, CURSOR, …, OTHER), externalId, url, model, repository, outputs, startedAt, endedAt, orn, sharedWithWorkspace | An AI agent session |
| `saveDocumentSource` | **workspaceOrn**, **name**, **content**, **extension**, orn, sharedWithWorkspace | A file (pdf, docx, md, …) |
| `saveImageSource` | **workspaceOrn**, **name**, **content** (base64), **extension** (jpg, png, …), orn, sharedWithWorkspace | An image |

## Collaboration

| Tool | Parameters | Use |
|------|------------|-----|
| `addComment` | **resourceOrn**, **workspaceOrn**, **content**, parentCommentOrn (reply), highlightText, highlightStartPosition, highlightEndPosition | Comment on a thought, note or source |
| `getNotifications` | **workspaceOrn**, typeFilter (MENTION/COMMENT/REACTION), isRead, page, pageSize | The user's notifications |
| `markNotificationsRead` | **workspaceOrn**, **notificationOrns** | Mark notifications read |
