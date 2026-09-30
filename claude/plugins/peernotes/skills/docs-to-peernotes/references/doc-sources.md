# Document sources: listing and reading

Use `<since>` = lookback start as an RFC 3339 timestamp.

## Google Drive

- **List**: search files with a query such as
  `modifiedTime > '<since>' and trashed = false and mimeType != 'application/vnd.google-apps.folder'`
  Add `'<folderId>' in parents` per selected folder (recurse into subfolders by listing child folders).
- **Read**:
  - Google Docs → read/export as plain text or markdown.
  - Google Sheets → export as XLSX (saved as a source) or CSV if the user wants it as a note table.
  - Google Slides → export as PDF (source).
  - Uploaded files (PDF, DOCX, images) → download content; DOCX/TXT/MD can be read as text, others become sources.
- **Metadata**: `id`, `name`, `mimeType`, `modifiedTime`, `owners`, `webViewLink`, `parents`.
- Google Meet transcripts and "Notes by Gemini" docs belong to the meeting-notes skill; skip them here if the meeting-notes sync is enabled.

## OneDrive / SharePoint

- **List**: list drive items in selected folders (recursively) or use search, filtering on `lastModifiedDateTime >= <since>`; skip items with a `folder` facet or `deleted` facet.
- **Read**: download content. Word/Markdown/TXT → text note; PDF/PowerPoint/Excel/images → source.
- **Metadata**: `id`, `name`, `file.mimeType`, `lastModifiedDateTime`, `createdBy`, `webUrl`, `parentReference.path`.

## Notion

- **List**: search pages (and database rows) with `last_edited_time` on or after `<since>`; for selected pages, include child pages recursively; for selected databases, query rows edited since `<since>`.
- **Read**: fetch the page content as markdown/blocks; include database properties as a small key–value table at the top.
- **Metadata**: page `id`, title, `last_edited_time`, `created_by`, `url`, parent.
- Skip archived pages.

## Change detection tips

- Compare source last-modified to the `Source modified:` line stored in the Peernotes source (decode its content).
- If the same document appears through two paths (e.g. a Drive shortcut), sync it once by ID.
