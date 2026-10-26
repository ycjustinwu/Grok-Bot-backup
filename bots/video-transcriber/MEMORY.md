# Video Transcriber — durable memory disaster-recovery backup

- Agent id: `8483d4a7-8144-46c8-900b-a55b5f17630a`
- Server id: `174592`
- Written: 2026-10-26 (HKT)
- Prior backup on disk: 2026-10-03 (this file overwritten for fleet backup request)
- User: Justin Wu
- Timezone: Asia/Hong_Kong

## Identity

- Name: Video Transcriber
- Title: empty (profile title field blank; agent profile section uses “Video Transcriber”)
- Description (ONE JOB): Drop a YouTube, Instagram, TikTok, or X link — get a clean transcript (plain text, SRT/VTT, optional speakers). Captions first; ASR only when needed.
- ANTI-JOBS: Do not write Cupsir / Deep content summaries when YouTube Analyzer Deep says they will write; do not invent dialogue; do not auto-send / auto-trade; do not paste secret values; do not enable Recursive Learning without Justin confirm.
- Avatar: default blob / black (no custom picture)
- Settings: `notifyOnAgentUpdates=true`; not hidden from sidebar
- Harness: temporal
- Role: Marketplace transcription specialist for YouTube, Instagram, TikTok, X, and video; caption-first, ASR fallback

### Partners / fleet handoffs

- **YouTube Analyzer Deep** (`5a056bd6-9373-4ff1-ab17-b1fa2a2d2e51`): primary consumer of Cupsir / Deep transcript handoffs. Reply with path + metadata; priority true when they are waiting to write.
- **總指揮** (`7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`): routing / usage-gate; Front-door Jev A stays OFF.
- **记忆管家** (`bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`): fleet memory backups.
- **Sweeper / 清道夫** (`8dbca7e8-e0d0-4447-821a-f9a3ad9d7e06`): stay-quiet clause on Recursive Learning.
- **Work Verifier** (`037de516-dbc1-4565-a127-5dbb0f691729`): transcript handoffs are generally not WV-gated; WV default pool (as of 2026-10-21) = Regime + US Market Daily Brief + 港股收市簡報 only.

### Jev (B+C) — TypeSafe

- Skill: [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` only — never paste secrets
- Log: `/workspace/typesafe-jev/logs/` when practical
- B pre-task: `act` | `evidence_enough` | `escalate` | `cost_tier` before grind
- C exit: `ready_for_justin` | `needs_wv` | `conflict` | `soft_ambition` before Final / handoff-out
- Note: client `.venv` was briefly missing mid-Oct 2026; as of 2026-10-26 backup check it is present again (`JEV_VENV_OK`)

## Historical decisions / locked rules

- (2026-09-08) Template import: created paused routine Recursive Learning (`0 8 * * 6`), wrote 8 journal memories, saved skills `video-to-transcript-pipeline` and `first-transcript`.
- (2026-09-08) First-run policy: ask only for a URL; presets `plain` | `timestamped` | `speakers` | `summary+quotes`; default `plain`.
- (2026-09-08) Default local ASR: faster-whisper + large-v3-turbo (EN) or large-v3 (multilingual); always prefer platform captions (manual over auto) before downloading audio.
- (2026-09-08) Production hygiene: `condition_on_previous_text=False`; Silero/VAD before ASR; 16 kHz mono; WhisperX for word timestamps / speakers; set min=max speakers only when count known.
- (2026-09-08) Output presets: plain (default), timestamped (SRT+VTT), speakers (diarized), summary+quotes; “everything” → speakers + timestamped + brief summary+quotes.
- (2026-09-14) Per Justin via Sweeper: appended stay-quiet clause to Recursive Learning prompt; left paused; schedule unchanged.
- (2026-09-14) Prior backup: `/workspace/174592-memory-backup.md`
- (2026-09-20) Standing usage gate (Justin via 總指揮): reuse a fresh artifact; stop after the same approach fails twice; chat-only when no tools are needed; prefer connector or API over clicking a site; do not create more bots or routines to save usage. Canon: `/workspace/fleet-policies/USAGE_GATE.md`.
- (2026-10) Cupsir / YAD deliverable paths:
  - Legacy Cupsir folder: `/workspace/cupsir-yt-analyzer/<id>-transcript.txt` (+ `.srt` / `.source.txt`)
  - Preferred YAD folder (current): `/workspace/youtube-analyzer-deep/<id>-transcript.txt` (+ `.srt` / `.vtt` / `.source.txt`)
- (2026-10) Caption recovery when `youtube_transcript_api` IpBlocked / `yt-dlp` 429: prefer ANDROID innertube (~20.10.38) → timedtext json3; Tavily watch-page extract as secondary; ASR last.
- (2026-10) YAD FYI acknowledgements (“收到…唔使再做”) need no reply; deliverable replies use priority true when YAD is waiting to write.
- (2026-10-21) WV default pool narrowed (shared): Regime + US Daily Brief + 港股收市簡報; transcripts not in default WV pool.

### Memory journal facts (tier: journal)

- (2026-09-08) As Video Transcriber (marketplace transcription specialist for YouTube, Instagram, TikTok, X, and video), default local ASR stack is faster-whisper with Whisper large-v3-turbo for English speed/accuracy balance, or large-v3 for non-English multilingual work; always prefer caption-first when platforms expose manual/auto captions before downloading audio. On first run, ask only for a URL and deliver with presets plain | timestamped | speakers | summary+quotes.
- (2026-09-08) Production transcription hygiene that is community-proven: set condition_on_previous_text=False; enable Silero/VAD filtering before ASR to cut silence hallucinations; feed 16 kHz mono WAV/audio; use WhisperX (faster-whisper + wav2vec2 alignment + pyannote) when word-level timestamps or speaker labels are required; set min_speakers=max_speakers only when speaker count is known (e.g. 2-person podcast), otherwise leave auto-detect.
- (2026-09-08) Output presets for every job: plain (default), timestamped (SRT+VTT), speakers (diarized transcript), summary+quotes (short summary + verbatim quotes + full plain transcript). If the user asks for everything, deliver speakers + timestamped + a brief summary+quotes block.
- (2026-09-08) Recursive Learning models: local default faster-whisper large-v3-turbo (EN) or large-v3 (multilingual); WhisperX for timestamps/diarization; Silero VAD; Parakeet TDT and Canary Qwen 2.5B for English GPU batch; MOSS-Transcribe-Diarize 0.9B for joint ASR+diarization.
- (2026-09-08) Recursive Learning APIs and pipeline: prefer AssemblyAI Universal-3.5 Pro, ElevenLabs Scribe v2, Gladia Solaria, Speechmatics Melia, or Groq Whisper turbo; always try platform captions first (manual over auto), then yt-dlp bestaudio to 16 kHz mono, ASR with condition_on_previous_text=False.
- (2026-09-08) Recursive Learning diarization: for local who-spoke-when, prefer WhisperX + pyannote 3.1/community-1, or DiariZen (BUT-FIT wavlm-large-s80-md-v2, better DER than pyannote 3.1 on AMI/AliMeeting/VoxConverse) paired with DiCoW for diarization-conditioned Whisper; Apache-2.0 pip package diarize (FoxNoseTech) is a CPU-only no-HF-token alternative (~10.8% DER VoxConverse). Set min_speakers=max_speakers only when speaker count is known; leave auto when unknown.
- (2026-09-08) Recursive Learning hosted ASR: OpenAI gpt-4o-transcribe-diarize on /v1/audio/transcriptions with response_format=diarized_json (optional known_speaker_names/references; no Realtime/streaming, ~1400s chunk limit); Deepgram Nova-3 with diarize_model=v2 for batch speaker labels (pin v2, not latest); keep AssemblyAI Universal-3.5 Pro, ElevenLabs Scribe v2, Gladia Solaria, Speechmatics Melia as top accuracy APIs; use Deepgram/AssemblyAI when streaming diarization is required.
- (2026-09-08) Recursive Learning open models: prefer nvidia/parakeet-tdt-0.6b-v3 for high-throughput multilingual ASR (25 European languages, auto language detect, timestamps, CC-BY-4.0) and nvidia/canary-1b-v2 when ASR plus EN bidirectional speech translation is needed; SoulX-Transcriber (Qwen3-Omni E2E SDR) is SOTA on Mandarin meeting benchmarks but still research/offline-heavy—not default production for English social video.

- Profile tier facts: none stored beyond Identity / Jev block in profile.json description.

## Live snapshot (2026-10-26)

### Routines

1. **Recursive Learning** — folder `76f92929-3c2c-547a-a108-1337bdb91114`
   - Schedule: `CRON_TZ=Asia/Hong_Kong 0 8 * * 6` (Every Saturday at 8:00 AM HKT)
   - Enabled: **paused** (`enabled: false`); never run
   - Prompt:
     > As an expert Transcription Specialist, find new tools and techniques the transcription community has tested and approved as powerful and bug-free. Learn those tips and techniques so your stack stays current. Summarize what changed and how you will apply it; surface useful findings to the user.
     >
     > If you find nothing new worth applying, stay quiet — do not send filler like "(no change.)".

### Skills

1. Video to transcript pipeline — id `video-to-transcript-pipeline`
2. First transcript — id `first-transcript`
3. Jev Fleet Decisions — id `jev-fleet-decisions` (fleet-shared)

### Stack preferences

- Caption-first (manual > auto), then ASR
- Local default: faster-whisper large-v3-turbo (EN) or large-v3 (multilingual)
- Proven YouTube caption bypass: ANDROID innertube timedtext json3
- Diarization: WhisperX + pyannote, or DiariZen ± DiCoW, or `diarize` CPU package
- Hosted: AssemblyAI Universal-3.5 Pro, ElevenLabs Scribe v2, Gladia Solaria, Speechmatics Melia, Groq Whisper turbo; OpenAI gpt-4o-transcribe-diarize; Deepgram Nova-3 diarize_model=v2

### Output / work paths

- `/workspace/youtube-analyzer-deep/` — current YAD handoff transcripts (examples present: `F3ItSTZNtT0`, `FQIH6o18y9g`, `QWzQo74cA7U`, `YLNqlY6Ut38`, `yJo3lWw66GI`, `yzk44lz-RGI`)
- `/workspace/cupsir-yt-analyzer/` — earlier Cupsir handoffs (examples: `oksfdsIMSl8`, `D-SVFneJ_Nk`, `sQaM5oPlUYs`, `6q_4jbedi7s`, `reWtEMpWlpA`, `JHo-aiePjoM`, `JnceIDVMZyQ`, `4axuNj63834`)
- Backup siblings: `/workspace/174592-memory-backup.md`; this file `/workspace/8483d4a7-8144-46c8-900b-a55b5f17630a-memory-backup.md`

### Open work

- No open transcript jobs as of backup write (2026-10-26).
- Latest completed YAD handoff in this thread arc: `yJo3lWw66GI` (Creative Planning; manual_captions; YAD confirmed used).

### Connectors / plugins

- None installed specifically for this bot; uses shared box tools (Shell, Tavily MCP when available, yt-dlp / innertube).

## Secrets

- No API keys or token **values** stored in this agent’s durable memory or this backup.
- Placeholders only:
  - `[REDACTED:TYPESAFE_API_KEY]` (Jev / TypeSafe — env only)
  - `[REDACTED:ASSEMBLYAI_API_KEY]`
  - `[REDACTED:ELEVENLABS_API_KEY]`
  - `[REDACTED:GLADIA_API_KEY]`
  - `[REDACTED:SPEECHMATICS_API_KEY]`
  - `[REDACTED:GROQ_API_KEY]`
  - `[REDACTED:OPENAI_API_KEY]`
  - `[REDACTED:DEEPGRAM_API_KEY]`
  - `[REDACTED:HUGGINGFACE_TOKEN]`
  - `[REDACTED:PROXY_URL]`

## Pending confirms

- Recursive Learning remains paused; Justin was asked whether to enable it — **no confirmed “turn on” yet**. List only; do not act.
- No other pending user confirms for this bot.
