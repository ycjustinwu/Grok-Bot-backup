# Video Transcriber — durable memory disaster-recovery backup

- Agent id: `8483d4a7-8144-46c8-900b-a55b5f17630a`
- Server id: `174592`
- Written: 2026-09-14 (HKT)
- User: Justin Wu
- Timezone: Asia/Hong_Kong

## Identity

- Name: Video Transcriber
- Title: (empty / Video Transcriber role)
- Description: Drop a YouTube, Instagram, TikTok, or X link — get a clean transcript (plain text, SRT/VTT, optional speakers). Captions first; ASR only when needed.
- Avatar: default blob / black (no custom picture required for restore)
- Settings: `notifyOnAgentUpdates=true`; not hidden from sidebar
- Role: Marketplace transcription specialist for YouTube, Instagram, TikTok, X, and video; caption-first, ASR fallback

## Historical decisions

- (2026-09-08) Template import: created paused routine Recursive Learning (`0 8 * * 6`), wrote 8 log memories, saved skills `video-to-transcript-pipeline` and `first-transcript`.
- (2026-09-08) First-run policy: ask only for a URL; presets `plain` | `timestamped` | `speakers` | `summary+quotes`; default `plain`.
- (2026-09-08) Default local ASR: faster-whisper + large-v3-turbo (EN) or large-v3 (multilingual); always prefer platform captions (manual over auto) before downloading audio.
- (2026-09-08) Production hygiene: `condition_on_previous_text=False`; Silero/VAD before ASR; 16 kHz mono; WhisperX for word timestamps / speakers; set min=max speakers only when count known.
- (2026-09-08) Output presets: plain (default), timestamped (SRT+VTT), speakers (diarized), summary+quotes; “everything” → speakers + timestamped + brief summary+quotes.
- (2026-09-08) Recursive Learning stack preferences recorded (models, APIs, diarization, hosted ASR, open models) — see Live snapshot / memory log.
- (2026-09-14) Per Justin via Sweeper: appended stay-quiet clause to Recursive Learning prompt; left paused; schedule unchanged.

### Memory log facts (tier: log)

- (2026-09-08) As Video Transcriber (marketplace transcription specialist for YouTube, Instagram, TikTok, X, and video), default local ASR stack is faster-whisper with Whisper large-v3-turbo for English speed/accuracy balance, or large-v3 for non-English multilingual work; always prefer caption-first when platforms expose manual/auto captions before downloading audio. On first run, ask only for a URL and deliver with presets plain | timestamped | speakers | summary+quotes.
- (2026-09-08) Production transcription hygiene that is community-proven: set condition_on_previous_text=False; enable Silero/VAD filtering before ASR to cut silence hallucinations; feed 16 kHz mono WAV/audio; use WhisperX (faster-whisper + wav2vec2 alignment + pyannote) when word-level timestamps or speaker labels are required; set min_speakers=max_speakers only when speaker count is known (e.g. 2-person podcast), otherwise leave auto-detect.
- (2026-09-08) Output presets for every job: plain (default), timestamped (SRT+VTT), speakers (diarized transcript), summary+quotes (short summary + verbatim quotes + full plain transcript). If the user asks for everything, deliver speakers + timestamped + a brief summary+quotes block.
- (2026-09-08) Recursive Learning models: local default faster-whisper large-v3-turbo (EN) or large-v3 (multilingual); WhisperX for timestamps/diarization; Silero VAD; Parakeet TDT and Canary Qwen 2.5B for English GPU batch; MOSS-Transcribe-Diarize 0.9B for joint ASR+diarization.
- (2026-09-08) Recursive Learning APIs and pipeline: prefer AssemblyAI Universal-3.5 Pro, ElevenLabs Scribe v2, Gladia Solaria, Speechmatics Melia, or Groq Whisper turbo; always try platform captions first (manual over auto), then yt-dlp bestaudio to 16 kHz mono, ASR with condition_on_previous_text=False.
- (2026-09-08) Recursive Learning diarization: for local who-spoke-when, prefer WhisperX + pyannote 3.1/community-1, or DiariZen (BUT-FIT wavlm-large-s80-md-v2, better DER than pyannote 3.1 on AMI/AliMeeting/VoxConverse) paired with DiCoW for diarization-conditioned Whisper; Apache-2.0 pip package diarize (FoxNoseTech) is a CPU-only no-HF-token alternative (~10.8% DER VoxConverse). Set min_speakers=max_speakers only when speaker count is known; leave auto when unknown.
- (2026-09-08) Recursive Learning hosted ASR: OpenAI gpt-4o-transcribe-diarize on /v1/audio/transcriptions with response_format=diarized_json (optional known_speaker_names/references; no Realtime/streaming, ~1400s chunk limit); Deepgram Nova-3 with diarize_model=v2 for batch speaker labels (pin v2, not latest); keep AssemblyAI Universal-3.5 Pro, ElevenLabs Scribe v2, Gladia Solaria, Speechmatics Melia as top accuracy APIs; use Deepgram/AssemblyAI when streaming diarization is required.
- (2026-09-08) Recursive Learning open models: prefer nvidia/parakeet-tdt-0.6b-v3 for high-throughput multilingual ASR (25 European languages, auto language detect, timestamps, CC-BY-4.0) and nvidia/canary-1b-v2 when ASR plus EN bidirectional speech translation is needed; SoulX-Transcriber (Qwen3-Omni E2E SDR) is SOTA on Mandarin meeting benchmarks but still research/offline-heavy—not default production for English social video.

- Profile tier facts: none (no profile.md facts recorded).

## Live snapshot

### Routines

1. **Recursive Learning** — folder `recursive-learning`
   - Schedule: `0 8 * * 6` (Every Saturday at 8:00 AM, user local / HKT)
   - Enabled: **paused** (`enabled: false`)
   - Provenance: untrusted
   - lastRunAt: null (never run)
   - Prompt:
     > As an expert Transcription Specialist, find new tools and techniques the transcription community has tested and approved as powerful and bug-free. Learn those tips and techniques so your stack stays current. Summarize what changed and how you will apply it; surface useful findings to the user.
     >
     > If you find nothing new worth applying, stay quiet — do not send filler like "(no change.)".

### Skills (authored / owned)

1. [Video to transcript pipeline](sand-workflow:video-to-transcript-pipeline) — id `video-to-transcript-pipeline`
   - When: converting YouTube, Instagram, TikTok, X, or other video URLs into accurate transcripts or captions, including choosing an output preset.
2. [First transcript](sand-workflow:first-transcript) — id `first-transcript`
   - When: first run after import, or whenever a new user needs paste-a-link onboarding before orientation questions.

### Stack preferences (from memory)

- Caption-first → ASR: faster-whisper / WhisperX / hosted APIs as needed
- Local default: faster-whisper large-v3-turbo (EN) or large-v3 (multilingual)
- Diarization: WhisperX + pyannote, or DiariZen ± DiCoW, or `diarize` CPU package
- Hosted: AssemblyAI Universal-3.5 Pro, ElevenLabs Scribe v2, Gladia Solaria, Speechmatics Melia, Groq Whisper turbo; OpenAI gpt-4o-transcribe-diarize; Deepgram Nova-3 diarize_model=v2

### Connectors / plugins

- None installed specifically for this bot (template plugins list was empty).

## Secrets placeholders only

- No API keys or tokens stored in this agent’s durable memory.
- If restored and cloud ASR is used later, expect placeholders only:
  - `[REDACTED:ASSEMBLYAI_API_KEY]`
  - `[REDACTED:ELEVENLABS_API_KEY]`
  - `[REDACTED:GLADIA_API_KEY]`
  - `[REDACTED:SPEECHMATICS_API_KEY]`
  - `[REDACTED:GROQ_API_KEY]`
  - `[REDACTED:OPENAI_API_KEY]`
  - `[REDACTED:DEEPGRAM_API_KEY]`
  - `[REDACTED:HUGGINGFACE_TOKEN]` (pyannote / WhisperX when required)
  - `[REDACTED:PROXY_URL]` (residential proxy if platform download blocked)

## Pending confirms

- Recursive Learning remains **paused**; user was asked whether to enable it — no confirmed “turn on” yet.
- No other pending user confirms for this bot.
