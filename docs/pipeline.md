# Pipeline Architecture

The Swanki pipeline orchestrates the complete process of converting academic PDFs into Anki flashcards with optional audio enhancement. The pipeline is configuration-driven using Hydra and supports various processing options and output formats.

## Main Pipeline Flow

```{mermaid}
graph TD
    %% Input Stage
    A[PDF Input] --> B{Initialize Pipeline}
    B --> |"Create output directory<br/>Set citation key"| C[Split PDF into Pages]
    
    %% PDF Processing Stage
    C --> D[Convert to Markdown<br/>via Mathpix]
    D --> |"Check conversion success"| E{Markdown Generated?}
    E -->|No| F[RuntimeError:<br/>Conversion Failed]
    E -->|Yes| G[Clean Markdown Files]
    
    %% Content Processing Stage
    G --> H[Process Images<br/>Extract & Summarize]
    H --> I[Generate Document Summary<br/>Early Context Creation]
    
    %% Card Generation Stage
    I --> J[Generate Text Cards<br/>Sliding Window Approach]
    I --> K{Image Cards<br/>Enabled?}
    K -->|Yes| L[Generate Image Cards<br/>Visual Content Testing]
    K -->|No| M[Skip Image Cards]
    
    J --> N[Combine All Cards]
    L --> N
    M --> N
    
    %% Output Generation Stage
    N --> O[Generate Output Files]
    O --> P[Plain Cards MD]
    O --> Q{Audio Enabled?}
    Q -->|Yes| R[Cards with Audio MD]
    Q -->|No| S[Skip Audio Cards File]
    O --> T[Document Summary MD]
    
    %% Audio Generation Stage
    Q -->|Complementary Audio| U[Generate Card Audio<br/>Front/Back for Each Card]
    Q -->|Summary Audio| V[Generate Summary Audio<br/>Document Overview]
    Q -->|Reading Audio| W[Generate Reading Audio<br/>Full Document TTS]
    Q -->|Lecture Audio| X[Generate Lecture Audio<br/>Educational Presentation]
    
    %% Anki Integration Stage
    U --> Y{Anki Integration<br/>Enabled?}
    V --> Y
    W --> Y
    X --> Y
    R --> Y
    S --> Y
    Y -->|Yes & Auto-Send| Z[Send to Anki<br/>via AnkiConnect]
    Y -->|No| AA[Pipeline Complete]
    Z --> AA
    
    %% Style definitions
    classDef inputClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef processClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef audioClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef outputClass fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef errorClass fill:#ffebee,stroke:#b71c1c,stroke-width:2px
    classDef decisionClass fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    
    class A inputClass
    class C,D,G,H,I,J,L processClass
    class U,V,W,X audioClass
    class P,R,T,AA outputClass
    class F errorClass
    class B,E,K,Q,Y decisionClass
```

## Pipeline Stages

### 1. PDF Processing

The pipeline begins by splitting the input PDF into individual pages using PyMuPDF. Each page is then converted to markdown using the Mathpix API, which preserves mathematical notation and formatting.

```{mermaid}
graph LR
    A[PDF Input] --> B[PDFProcessor]
    B --> C[Split PDF]
    C --> D[Individual Pages<br/>page-1.pdf, page-2.pdf...]
    D --> E[MarkdownConverter]
    E --> F[Mathpix API]
    F --> G[Markdown Files<br/>page-1.md, page-2.md...]
    
    style A fill:#e1f5fe
    style G fill:#e8f5e9
```

### 2. Content Processing

Raw markdown files are cleaned to remove artifacts and standardize formatting. Images are extracted and summarized using AI to provide context for card generation.

```{mermaid}
graph TD
    A[Raw Markdown Files] --> B[MarkdownCleaner]
    B --> C[Clean Markdown Files]
    C --> D[ImageProcessor]
    D --> E[Extract Images]
    E --> F[Generate Image Summaries<br/>Using OpenAI]
    C --> G[Content Combiner]
    F --> G
    G --> H[Document Summary Generator]
    H --> I[Structured DocumentSummary<br/>- Title<br/>- Authors<br/>- Key Contributions<br/>- Acronyms<br/>- Technical Terms]
    
    style A fill:#fff3e0
    style I fill:#e8f5e9
```

### 3. Card Generation

Cards are generated using a sliding window approach for better context. Both text-based and image-based cards are supported with various placement strategies. See the [Sliding Window Processing](configuration.md#sliding-window-processing) section in the configuration guide for detailed information on how to configure window sizes and skip parameters.

```{mermaid}
graph TD
    A[Document Summary<br/>+ Clean Markdown] --> B{Card Generation}
    B --> C[Text Card Generation]
    C --> D[Sliding Window<br/>window_size: 2<br/>skip: 1]
    D --> E[Combine Window Content]
    E --> F[Generate Cards<br/>via Instructor/OpenAI]
    
    B --> G[Image Card Generation]
    G --> H[Extract Images<br/>with Context]
    H --> I{Placement Strategy}
    I -->|Smart| J[Analyze Question<br/>for Image Reference]
    I -->|Alternate| K[Alternate Front/Back]
    I -->|Random| L[Random with Ratio]
    I -->|Prefer Front/Back| M[Fixed Placement]
    
    F --> N[PlainCard Objects]
    J --> N
    K --> N
    L --> N
    M --> N
    
    style A fill:#e1f5fe
    style N fill:#e8f5e9
```

### 4. Audio Generation

Multiple audio types can be generated with configurable speed settings. Audio is created using ElevenLabs TTS with pitch-preserved speed adjustment.

```{mermaid}
graph TD
    A[Audio Configuration] --> B{Audio Types}
    
    B -->|Complementary| C[Card Audio Generation]
    C --> D[For Each Card]
    D --> E[Generate Front Transcript<br/>with Citation Key]
    D --> F[Generate Back Transcript<br/>Handle Cloze Masking]
    E --> G[TTS via ElevenLabs<br/>Apply Speed Setting]
    F --> G
    
    B -->|Summary| H[Summary Audio]
    H --> I[Format Summary Text]
    I --> J[TTS Generation<br/>Apply Speed Setting]
    
    B -->|Reading| K[Reading Audio]
    K --> L[Combine All Content]
    L --> M[Generate Reading Transcript]
    M --> N[TTS in Chunks<br/>Apply Speed Setting]
    
    B -->|Lecture| O[Lecture Audio]
    O --> P[Create Educational Script]
    P --> Q[TTS Generation<br/>Apply Speed Setting]
    
    G --> R[Audio Files<br/>MP3 Format]
    J --> R
    N --> R
    Q --> R
    
    style A fill:#fff9c4
    style R fill:#e8f5e9
```

### 5. Anki Integration

Cards can be automatically sent to Anki using AnkiConnect. The system handles deck creation, card updates, and media file uploads.

```{mermaid}
graph TD
    A[Generated Cards] --> B{Anki Config}
    B --> C[Format Deck Name<br/>Template: {citation_key}]
    C --> D[Choose Card Format]
    D -->|Plain| E[Use cards-plain.md]
    D -->|With Audio| F[Use cards-with-audio.md]
    
    E --> G[Prepare Anki File<br/>Add Deck Header]
    F --> G
    
    G --> H[AnkiProcessor]
    H --> I[AnkiConnect API]
    I --> J{Actions}
    J --> K[Create/Select Deck]
    J --> L[Add/Update Cards]
    J --> M[Upload Media Files]
    J --> N[Sync Collection]
    
    K --> O[Success Response]
    L --> O
    M --> O
    N --> O
    
    style A fill:#e1f5fe
    style O fill:#e8f5e9
```

## Configuration System

The pipeline is highly configurable using Hydra. Configuration files are automatically generated with sensible defaults.

```{mermaid}
graph TD
    A[User Command] --> B[Hydra Config System]
    B --> C[ConfigGenerator]
    C --> D{Config Exists?}
    D -->|No| E[Generate Default Configs<br/>~/.swanki_config/]
    D -->|Yes| F[Load User Configs]
    
    E --> G[Merge Configurations]
    F --> G
    
    G --> H[Pipeline Configuration]
    H --> I[Processing Config<br/>- window_size<br/>- num_cards_per_page<br/>- image_cards settings]
    H --> J[Audio Config<br/>- generate flags<br/>- speed settings<br/>- voice settings]
    H --> K[Prompts Config<br/>- system prompts<br/>- generation prompts]
    H --> L[Models Config<br/>- LLM settings<br/>- TTS settings]
    H --> M[Output Config<br/>- file formats<br/>- tag formats]
    H --> N[Anki Config<br/>- deck settings<br/>- auto-send options]
    
    style A fill:#e1f5fe
    style H fill:#e8f5e9
```

## Key Features

1. **Configuration-Driven**: All aspects controlled via Hydra configs
2. **Sliding Window Processing**: Better context for card generation
3. **Early Summary Generation**: Provides context for all downstream processing
4. **Flexible Audio Options**: Multiple audio types with speed control
5. **Smart Image Card Generation**: Various placement strategies
6. **Robust Error Handling**: Graceful degradation and recovery
7. **Anki Integration**: Direct upload via AnkiConnect

## Usage Examples

### Basic Pipeline
```bash
swanki --pdf_path=paper.pdf --citation_key=Smith2023
```

### With Custom Output Directory
```bash
swanki --pdf_path=paper.pdf --citation_key=Smith2023 +output_dir=chapter1
```

### Full Audio Generation
```bash
swanki --pdf_path=paper.pdf --citation_key=Smith2023 \
       audio.audio.generate_complementary=true \
       audio.audio.generate_summary=true \
       audio.audio.generate_reading=true \
       audio.audio.generate_lecture=true
```

### Custom Processing Options
```bash
swanki --pdf_path=paper.pdf --citation_key=Smith2023 \
       pipeline.processing.window_size=3 \
       pipeline.processing.num_cards_per_page=5 \
       audio.audio.complementary_speed=1.6
```