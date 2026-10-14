2,949 files, 81 MB — identical file counts, sizes and checksums to the source. I ran a search from inside the copy to confirm it stands alone: it returns the WB_CLK answer from both the Wishbone notes and TRM page 340, and the index reports its full 2,739 documents / 8,467 chunks.

What included:

File	What it does for them
CLAUDE.md	Picked up automatically by Claude Code — folder map, instructions to search before answering and cite file and page, verified facts
README.md	Directory structure, quick start, limitations, provenance
GETTING_STARTED.md	The short version
knowledge_base/	53 documents; knowledge_base/README.md is the index
source_code_knowledge/	QuickLogic’s code as reference
kb_search/	Search scripts plus the prebuilt kb.sqlite, so they don’t have to rebuild

They copy the folder locally, run claude in it, and ask questions. Only Python 3.8+ is needed — no install, no key, no network.


I put it inside the EOS working folder, because W:\2026\EOS is the only path connected to this session. If you’d rather it sat alongside rather than inside your working tree — say W:\2026\eos-s3-kb — grant me access to W:\2026 and I’ll move it.
The prebuilt index is included, which is why it’s 81 MB rather than 31 MB. That’s the trade for the colleague being able to search immediately. If they edit or add documents they rerun python kb_search/build_index.py, about a minute.
Check redistribution before it travels far. The TRM conversion is in there, and the original is marked for restricted distribution. Fine for a QuickLogic colleague; the README has the commands to drop that one file if it needs to go wider.