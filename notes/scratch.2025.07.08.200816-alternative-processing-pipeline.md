---
id: pipo5c8af5lgobuuofkfr5y
title: 200816 Alternative Processing Pipeline
desc: ''
updated: 1752023306375
created: 1752023306375
---

# DAG-Based Document Decomposition Pipeline for Swanki

## Overview & Motivation

The current sliding window approach treats documents linearly, missing the hierarchical structure of knowledge. This alternative pipeline decomposes documents into a Directed Acyclic Graph (DAG) that mirrors how experts organize and understand complex material.

### Key Innovations

1. **Hierarchical Knowledge Graph**: Documents are decomposed into a multi-level DAG from abstract summaries to specific details
2. **Two-Dimensional Card Generation**: Cards vary by both graph depth (conceptual level) and difficulty (cognitive demand)
3. **Candidate Generation with Critic**: Multiple card candidates are generated and evaluated by an AI critic
4. **Self-Verification**: Ensures correctness using forward reasoning and backward verification
5. **Complete Mastery Focus**: Covers all aspects needed for subject mastery

## Core Architecture

### Data Models (Using Instructor/Pydantic)

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from enum import Enum
import instructor
from openai import OpenAI

# Initialize instructor
client = instructor.from_openai(OpenAI())

class NodeType(str, Enum):
    ROOT = "root"
    CHAPTER = "chapter"
    CONCEPT = "concept"
    DETAIL = "detail"
    DEFINITION = "definition"
    THEOREM = "theorem"
    PROOF = "proof"
    EXAMPLE = "example"
    HISTORICAL = "historical"

class DifficultyLevel(str, Enum):
    RECALL = "recall"  # Simple fact retrieval
    COMPREHENSION = "comprehension"  # Understanding meaning
    APPLICATION = "application"  # Using in new contexts
    ANALYSIS = "analysis"  # Breaking down components
    SYNTHESIS = "synthesis"  # Creating new connections
    EVALUATION = "evaluation"  # Making judgments

class ConceptNode(BaseModel):
    """Node in the document knowledge graph"""
    node_id: str
    node_type: NodeType
    level: int = Field(..., description="0=root, 1=chapter, 2=concept, 3=detail")
    title: str
    content_refs: List[Dict[str, int]] = Field(
        ..., 
        description="References to original document [{page: X, start_char: Y, end_char: Z}]"
    )
    summary: str = Field(..., max_length=500)
    importance_score: float = Field(..., ge=0, le=1)
    
    # Relationships
    parent_id: Optional[str] = None
    children_ids: List[str] = Field(default_factory=list)
    prerequisite_ids: List[str] = Field(default_factory=list)
    related_ids: List[str] = Field(default_factory=list)
    
    # Content metadata
    contains_math: bool = False
    contains_code: bool = False
    key_terms: List[str] = Field(default_factory=list)
    
    # For theorems/proofs
    formal_statement: Optional[str] = None
    proof_steps: Optional[List[str]] = None

class CardCandidate(BaseModel):
    """A potential flashcard for a concept"""
    card_id: str
    node_id: str
    depth_level: int
    difficulty: DifficultyLevel
    card_type: Literal["regular", "cloze", "image"]
    
    question: str
    answer: str
    
    # Metadata for critic evaluation
    tests_understanding: bool = Field(..., description="Does this test conceptual understanding?")
    self_contained: bool = Field(..., description="Can be understood without external context?")
    pedagogical_value: float = Field(..., ge=0, le=1)
    
    # Prerequisites and relationships
    prerequisite_concepts: List[str] = Field(default_factory=list)
    related_cards: List[str] = Field(default_factory=list)
    
    # Tags
    tags: List[str] = Field(default_factory=list)

class CriticEvaluation(BaseModel):
    """Critic's evaluation of a card candidate"""
    card_id: str
    overall_score: float = Field(..., ge=0, le=1)
    
    # Detailed scores
    clarity_score: float = Field(..., ge=0, le=1)
    difficulty_appropriate: bool
    tests_key_concept: bool
    avoids_triviality: bool
    
    # Feedback
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    
    # Decision
    selected: bool
    selection_reason: str

class DocumentDAG(BaseModel):
    """Complete document knowledge graph"""
    document_id: str
    title: str
    root_node_id: str
    
    nodes: Dict[str, ConceptNode] = Field(default_factory=dict)
    
    # Learning paths through the DAG
    suggested_paths: List[List[str]] = Field(
        default_factory=list,
        description="Topologically sorted learning paths"
    )
    
    # Metadata
    total_concepts: int = 0
    max_depth: int = 0
    coverage_score: float = Field(0.0, description="How well we've covered the document")
```

### Document Analysis and DAG Construction

```python
class DocumentAnalyzer:
    """Analyzes document structure and extracts hierarchical concepts"""
    
    def __init__(self, instructor_client):
        self.client = instructor_client
    
    def analyze_document(self, markdown_files: List[Path]) -> DocumentStructure:
        """
        Extract document structure using LLM
        
        Pseudocode:
        1. Combine markdown files
        2. Extract major sections/chapters
        3. Identify concept hierarchy
        4. Detect special content (proofs, theorems, definitions)
        """
        
        class DocumentStructure(BaseModel):
            title: str
            chapters: List[Chapter]
            key_concepts: List[str]
            document_type: Literal["textbook", "paper", "notes", "mixed"]
            has_proofs: bool
            has_code: bool
            estimated_nodes: int
        
        class Chapter(BaseModel):
            title: str
            page_range: tuple[int, int]
            main_concepts: List[str]
            sub_sections: List[str]
        
        combined_content = self._combine_markdown(markdown_files)
        
        structure = self.client.chat.completions.create(
            model="gpt-4",
            response_model=DocumentStructure,
            messages=[{
                "role": "system",
                "content": "You are an expert at analyzing academic document structure."
            }, {
                "role": "user", 
                "content": f"""
                Analyze this document's structure and identify:
                1. Main chapters/sections
                2. Key concepts in each section
                3. Document type
                4. Special content (proofs, code, etc.)
                
                Document:
                {combined_content[:10000]}  # First 10k chars
                """
            }]
        )
        
        return structure

class DAGBuilder:
    """Constructs knowledge DAG from document analysis"""
    
    def build_dag(self, document_structure: DocumentStructure, 
                  markdown_files: List[Path]) -> DocumentDAG:
        """
        Build hierarchical DAG
        
        Pseudocode:
        1. Create root node (document summary)
        2. Create chapter nodes
        3. Extract concepts within chapters
        4. Create detail nodes for specific items
        5. Establish relationships
        """
        
        # Step 1: Create root node
        root = self._create_root_node(document_structure)
        
        # Step 2: Create chapter-level nodes
        chapter_nodes = []
        for chapter in document_structure.chapters:
            node = self._create_chapter_node(chapter, parent_id=root.node_id)
            chapter_nodes.append(node)
        
        # Step 3: Extract concepts for each chapter
        for chapter_node in chapter_nodes:
            concepts = self._extract_chapter_concepts(
                chapter_node, 
                markdown_files[chapter.page_range[0]:chapter.page_range[1]]
            )
            
            # Step 4: Extract details for each concept
            for concept in concepts:
                details = self._extract_concept_details(concept)
                concept.children_ids.extend([d.node_id for d in details])
        
        # Step 5: Establish cross-references and prerequisites
        self._establish_relationships(all_nodes)
        
        return DocumentDAG(nodes=all_nodes, ...)
    
    def _extract_chapter_concepts(self, chapter_node: ConceptNode, 
                                  content: str) -> List[ConceptNode]:
        """Extract key concepts from a chapter"""
        
        class ConceptExtraction(BaseModel):
            concepts: List[ExtractedConcept]
        
        class ExtractedConcept(BaseModel):
            title: str
            summary: str
            content_snippet: str
            is_definition: bool
            is_theorem: bool
            is_example: bool
            contains_math: bool
            importance: float = Field(..., ge=0, le=1)
        
        extraction = self.client.chat.completions.create(
            model="gpt-4",
            response_model=ConceptExtraction,
            messages=[{
                "role": "system",
                "content": """Extract key concepts from this chapter. Include:
                - Main ideas and methods
                - Definitions
                - Theorems and lemmas
                - Important examples
                Rate importance 0-1 based on centrality to understanding."""
            }, {
                "role": "user",
                "content": f"Chapter: {chapter_node.title}\n\n{content}"
            }]
        )
        
        # Convert to ConceptNodes
        concept_nodes = []
        for ec in extraction.concepts:
            node = ConceptNode(
                node_id=f"{chapter_node.node_id}_c{len(concept_nodes)}",
                node_type=self._determine_node_type(ec),
                level=2,  # Concept level
                title=ec.title,
                summary=ec.summary,
                parent_id=chapter_node.node_id,
                importance_score=ec.importance,
                contains_math=ec.contains_math
            )
            concept_nodes.append(node)
        
        return concept_nodes
```

## Two-Dimensional Card Generation

### Card Generation Strategy

```python
class HierarchicalCardGenerator:
    """Generates cards at different depths and difficulties"""
    
    def generate_cards_for_node(self, node: ConceptNode, 
                               dag: DocumentDAG,
                               num_candidates: int = 5) -> List[CardCandidate]:
        """
        Generate multiple card candidates for a node
        
        Cards vary by:
        1. Depth level (which node in the hierarchy)
        2. Difficulty (cognitive complexity)
        """
        
        candidates = []
        
        # Generate cards at each difficulty level
        for difficulty in DifficultyLevel:
            prompt = self._build_card_prompt(node, dag, difficulty)
            
            class CardBatch(BaseModel):
                cards: List[GeneratedCard]
            
            class GeneratedCard(BaseModel):
                question: str
                answer: str
                tests_understanding: bool
                self_contained: bool
                key_insight: str
            
            batch = self.client.chat.completions.create(
                model="gpt-4",
                response_model=CardBatch,
                messages=[{
                    "role": "system",
                    "content": self._get_system_prompt(difficulty)
                }, {
                    "role": "user",
                    "content": prompt
                }],
                n=num_candidates  # Generate multiple versions
            )
            
            # Convert to CardCandidates
            for i, gc in enumerate(batch.cards):
                candidate = CardCandidate(
                    card_id=f"{node.node_id}_d{difficulty.value}_v{i}",
                    node_id=node.node_id,
                    depth_level=node.level,
                    difficulty=difficulty,
                    card_type="regular",
                    question=gc.question,
                    answer=gc.answer,
                    tests_understanding=gc.tests_understanding,
                    self_contained=gc.self_contained,
                    pedagogical_value=self._estimate_pedagogical_value(gc),
                    tags=self._generate_tags(node, difficulty)
                )
                candidates.append(candidate)
        
        return candidates
    
    def _get_system_prompt(self, difficulty: DifficultyLevel) -> str:
        """Get difficulty-specific system prompts"""
        
        prompts = {
            DifficultyLevel.RECALL: """
                Create simple factual questions that test basic memory.
                Focus on definitions, names, dates, and simple facts.
                Example: "What is the definition of a DAG?"
            """,
            
            DifficultyLevel.COMPREHENSION: """
                Create questions that test understanding of concepts.
                Ask about meaning, interpretation, and basic relationships.
                Example: "Why must a DAG not contain cycles?"
            """,
            
            DifficultyLevel.APPLICATION: """
                Create questions that require applying concepts to new situations.
                Include simple problem-solving and usage examples.
                Example: "Given nodes A→B→C and A→C, is this a valid DAG? Why?"
            """,
            
            DifficultyLevel.ANALYSIS: """
                Create questions that require breaking down complex ideas.
                Focus on components, relationships, and systematic thinking.
                Example: "Compare the time complexity of DFS vs topological sort for DAG traversal"
            """,
            
            DifficultyLevel.SYNTHESIS: """
                Create questions that require combining multiple concepts.
                Focus on creating new connections and solving complex problems.
                Example: "Design an algorithm to find the longest path in a DAG"
            """,
            
            DifficultyLevel.EVALUATION: """
                Create questions requiring judgment and critical thinking.
                Focus on trade-offs, optimality, and design decisions.
                Example: "Evaluate the choice of using a DAG vs tree for representing course prerequisites"
            """
        }
        
        return prompts[difficulty]
```

### Multi-Level Card Examples

```python
def generate_hierarchical_cards_example():
    """Example of cards at different levels for NOTEARS paper"""
    
    # ROOT LEVEL (Document Summary)
    root_cards = [
        CardCandidate(
            depth_level=0,
            difficulty=DifficultyLevel.COMPREHENSION,
            question="What is the key innovation of NOTEARS for learning DAGs?",
            answer="""NOTEARS reformulates the combinatorial DAG learning problem 
                     as a continuous optimization problem by introducing a smooth 
                     acyclicity constraint h(W) = tr(e^W) - d that equals 0 iff 
                     W represents a DAG, enabling gradient-based optimization."""
        ),
    ]
    
    # CONCEPT LEVEL (Acyclicity Constraint)
    concept_cards = [
        CardCandidate(
            depth_level=2,
            difficulty=DifficultyLevel.RECALL,
            question="What is the NOTEARS acyclicity constraint formula?",
            answer="h(W) = tr(e^W) - d, where W is the weighted adjacency matrix and d is the number of nodes"
        ),
        CardCandidate(
            depth_level=2,
            difficulty=DifficultyLevel.APPLICATION,
            question="Given a 3×3 matrix W with a cycle A→B→C→A, what is the sign of h(W)?",
            answer="h(W) > 0, because h(W) = 0 only when W represents a DAG (no cycles)"
        ),
    ]
    
    # DETAIL LEVEL (Specific Properties)
    detail_cards = [
        CardCandidate(
            depth_level=3,
            difficulty=DifficultyLevel.ANALYSIS,
            question="Why is the gradient ∇h(W) = (e^W)^T for the acyclicity constraint?",
            answer="""By matrix calculus: ∇tr(e^W) = (e^W)^T and ∇d = 0,
                     so ∇h(W) = ∇tr(e^W) - ∇d = (e^W)^T"""
        ),
    ]
```

## Card Candidate Selection with Critic

### Critic System

```python
class CardCritic:
    """Evaluates and selects best card candidates"""
    
    def __init__(self, learning_goals: LearningGoals):
        self.learning_goals = learning_goals
        self.client = instructor.from_openai(OpenAI())
    
    def evaluate_candidates(self, 
                          candidates: List[CardCandidate],
                          node: ConceptNode,
                          dag: DocumentDAG) -> List[CriticEvaluation]:
        """Evaluate each candidate against learning goals"""
        
        evaluations = []
        
        for candidate in candidates:
            eval_prompt = f"""
            Evaluate this flashcard for learning {node.title}:
            
            Question: {candidate.question}
            Answer: {candidate.answer}
            
            Node Context: {node.summary}
            Difficulty: {candidate.difficulty}
            Depth Level: {candidate.depth_level}
            
            Learning Goals:
            - Mastery Level: {self.learning_goals.mastery_level}
            - Focus Areas: {self.learning_goals.focus_areas}
            - Avoid: {self.learning_goals.avoid_areas}
            
            Evaluate on:
            1. Clarity and self-containment
            2. Appropriate difficulty
            3. Tests key concepts (not trivia)
            4. Pedagogical value
            5. Alignment with learning goals
            """
            
            evaluation = self.client.chat.completions.create(
                model="gpt-4",
                response_model=CriticEvaluation,
                messages=[{
                    "role": "system",
                    "content": """You are an expert educational content critic.
                                 Evaluate flashcards for their learning effectiveness."""
                }, {
                    "role": "user",
                    "content": eval_prompt
                }]
            )
            
            evaluation.card_id = candidate.card_id
            evaluations.append(evaluation)
        
        return evaluations
    
    def select_best_cards(self,
                         evaluations: List[CriticEvaluation],
                         target_count: int) -> List[str]:
        """Select best cards based on evaluations"""
        
        # Sort by overall score
        sorted_evals = sorted(evaluations, 
                            key=lambda e: e.overall_score, 
                            reverse=True)
        
        selected_ids = []
        difficulty_counts = {d: 0 for d in DifficultyLevel}
        
        # Select with diversity constraints
        for eval in sorted_evals:
            if len(selected_ids) >= target_count:
                break
                
            candidate = self._get_candidate(eval.card_id)
            
            # Ensure difficulty diversity
            if difficulty_counts[candidate.difficulty] < target_count // len(DifficultyLevel) + 1:
                selected_ids.append(eval.card_id)
                difficulty_counts[candidate.difficulty] += 1
                eval.selected = True
                eval.selection_reason = f"High score ({eval.overall_score:.2f}) with good difficulty balance"
        
        return selected_ids
```

### Self-Verification Integration

```python
class CardVerifier:
    """Verifies card correctness using self-verification"""
    
    def verify_card(self, card: CardCandidate, context: str) -> VerificationResult:
        """
        Implement self-verification as shown in instructor docs
        
        1. Forward reasoning - generate multiple answers
        2. Backward verification - verify each answer
        """
        
        class AnswerCandidate(BaseModel):
            reasoning_steps: List[str]
            answer: str
        
        class VerificationResult(BaseModel):
            original_answer: str
            verified_answer: str
            confidence_score: float
            verification_steps: List[str]
            is_correct: bool
        
        # Step 1: Generate multiple answer candidates
        n_candidates = 3
        candidates = []
        
        for _ in range(n_candidates):
            candidate = self.client.chat.completions.create(
                model="gpt-4",
                response_model=AnswerCandidate,
                messages=[{
                    "role": "user",
                    "content": f"""
                    Context: {context}
                    Question: {card.question}
                    
                    Provide step-by-step reasoning and answer.
                    """
                }]
            )
            candidates.append(candidate)
        
        # Step 2: Backward verification for each candidate
        verification_scores = []
        
        for candidate in candidates:
            # Rewrite as declarative statement
            declarative = self._rewrite_as_declarative(
                card.question, 
                candidate.answer
            )
            
            # Verify k times
            k = 5
            correct_count = 0
            
            for _ in range(k):
                verification = self.client.chat.completions.create(
                    model="gpt-4",
                    response_model=BooleanVerification,
                    messages=[{
                        "role": "user",
                        "content": f"""
                        Given the context: {context}
                        
                        Is this statement correct? (Answer True or False)
                        {declarative}
                        """
                    }]
                )
                
                if verification.is_correct:
                    correct_count += 1
            
            verification_scores.append((candidate, correct_count / k))
        
        # Select best candidate
        best_candidate, best_score = max(verification_scores, key=lambda x: x[1])
        
        return VerificationResult(
            original_answer=card.answer,
            verified_answer=best_candidate.answer,
            confidence_score=best_score,
            verification_steps=best_candidate.reasoning_steps,
            is_correct=best_score > 0.8
        )
```

### Self-Refine Integration

```python
class CardRefiner:
    """Iteratively improve cards using self-refine pattern"""
    
    def refine_card(self, card: CardCandidate, max_iterations: int = 3) -> CardCandidate:
        """
        Apply self-refine pattern from instructor docs
        """
        
        class CardFeedback(BaseModel):
            feedback_points: List[str]
            improvement_suggestions: List[str]
            clarity_score: float = Field(..., ge=0, le=1)
            pedagogy_score: float = Field(..., ge=0, le=1)
            done: bool = Field(..., description="True if card is good enough")
        
        current_card = card
        history = []
        
        for iteration in range(max_iterations):
            # Generate feedback
            feedback = self.client.chat.completions.create(
                model="gpt-4",
                response_model=CardFeedback,
                messages=[{
                    "role": "system",
                    "content": """You are an expert flashcard reviewer.
                                 Provide specific feedback to improve this card."""
                }, {
                    "role": "user",
                    "content": f"""
                    Review this flashcard:
                    
                    Question: {current_card.question}
                    Answer: {current_card.answer}
                    Difficulty: {current_card.difficulty}
                    
                    Check for:
                    1. Clarity and precision
                    2. Self-containment
                    3. Appropriate difficulty
                    4. Pedagogical value
                    5. No external references
                    
                    If the card is excellent, set done=True.
                    """
                }]
            )
            
            if feedback.done:
                break
            
            # Refine based on feedback
            refined_card = self.client.chat.completions.create(
                model="gpt-4",
                response_model=RefinedCard,
                messages=[{
                    "role": "user",
                    "content": f"""
                    Improve this flashcard based on feedback:
                    
                    Original:
                    Q: {current_card.question}
                    A: {current_card.answer}
                    
                    Feedback:
                    {chr(10).join(feedback.feedback_points)}
                    
                    Suggestions:
                    {chr(10).join(feedback.improvement_suggestions)}
                    
                    Generate an improved version.
                    """
                }]
            )
            
            # Update current card
            current_card.question = refined_card.question
            current_card.answer = refined_card.answer
            
            history.append({
                "iteration": iteration,
                "feedback": feedback,
                "refined": refined_card
            })
        
        return current_card
```

## Complete Processing Pipeline

```python
class DAGProcessingPipeline:
    """Main pipeline for DAG-based document processing"""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.client = instructor.from_openai(OpenAI())
        
        # Initialize components
        self.analyzer = DocumentAnalyzer(self.client)
        self.dag_builder = DAGBuilder(self.client)
        self.card_generator = HierarchicalCardGenerator(self.client)
        self.critic = CardCritic(config.learning_goals)
        self.verifier = CardVerifier(self.client)
        self.refiner = CardRefiner(self.client)
    
    def process_document(self, 
                        markdown_files: List[Path],
                        citation_key: str) -> ProcessingResult:
        """
        Complete pipeline execution
        
        Pseudocode:
        1. Analyze document structure
        2. Build knowledge DAG
        3. Generate card candidates for each node
        4. Evaluate and select best cards
        5. Verify and refine selected cards
        6. Create final output
        """
        
        # Step 1: Document Analysis
        print("Analyzing document structure...")
        doc_structure = self.analyzer.analyze_document(markdown_files)
        
        # Step 2: Build DAG
        print("Building knowledge graph...")
        dag = self.dag_builder.build_dag(doc_structure, markdown_files)
        print(f"Created DAG with {len(dag.nodes)} nodes, max depth {dag.max_depth}")
        
        # Step 3: Generate candidates for each node
        print("Generating card candidates...")
        all_candidates = {}
        
        for node_id, node in dag.nodes.items():
            # Skip if below importance threshold
            if node.importance_score < self.config.min_importance:
                continue
            
            # Generate more candidates for important nodes
            num_candidates = int(5 * (1 + node.importance_score))
            
            candidates = self.card_generator.generate_cards_for_node(
                node, dag, num_candidates
            )
            
            all_candidates[node_id] = candidates
            print(f"Generated {len(candidates)} candidates for {node.title}")
        
        # Step 4: Critic evaluation and selection
        print("Evaluating candidates with critic...")
        selected_cards = []
        
        for node_id, candidates in all_candidates.items():
            node = dag.nodes[node_id]
            
            # Evaluate all candidates
            evaluations = self.critic.evaluate_candidates(
                candidates, node, dag
            )
            
            # Determine target count based on node importance
            target_count = self._calculate_target_cards(node)
            
            # Select best cards
            selected_ids = self.critic.select_best_cards(
                evaluations, target_count
            )
            
            # Get selected cards
            node_cards = [c for c in candidates if c.card_id in selected_ids]
            selected_cards.extend(node_cards)
        
        print(f"Selected {len(selected_cards)} cards from {sum(len(c) for c in all_candidates.values())} candidates")
        
        # Step 5: Verify and refine
        print("Verifying and refining cards...")
        final_cards = []
        
        for card in selected_cards:
            # Verify correctness
            node = dag.nodes[card.node_id]
            context = self._get_node_context(node, dag)
            
            verification = self.verifier.verify_card(card, context)
            
            if not verification.is_correct:
                print(f"Card {card.card_id} failed verification, updating...")
                card.answer = verification.verified_answer
            
            # Refine for quality
            refined_card = self.refiner.refine_card(card)
            final_cards.append(refined_card)
        
        # Step 6: Create output
        print("Creating final output...")
        return ProcessingResult(
            dag=dag,
            cards=final_cards,
            statistics=self._calculate_statistics(dag, final_cards)
        )
    
    def _calculate_target_cards(self, node: ConceptNode) -> int:
        """Calculate how many cards to generate for a node"""
        
        base_count = {
            0: 5,  # Root level
            1: 4,  # Chapter level  
            2: 3,  # Concept level
            3: 2   # Detail level
        }.get(node.level, 2)
        
        # Adjust by importance
        importance_multiplier = 1 + node.importance_score
        
        # Adjust by node type
        type_multiplier = {
            NodeType.THEOREM: 1.5,
            NodeType.DEFINITION: 1.3,
            NodeType.PROOF: 1.4,
            NodeType.EXAMPLE: 0.8
        }.get(node.node_type, 1.0)
        
        return int(base_count * importance_multiplier * type_multiplier)
```

## Configuration Schema

```yaml
# dag_decomposition.yaml
processing:
  strategy: "dag_decomposition"
  
  # Document analysis
  analysis:
    min_concept_size: 50  # Minimum words for a concept
    max_depth: 4  # Maximum DAG depth
    importance_threshold: 0.3  # Minimum importance to process
    
  # DAG construction
  dag:
    merge_similar_concepts: true
    similarity_threshold: 0.85
    establish_prerequisites: true
    
  # Card generation
  cards:
    candidates_per_node: 5
    difficulty_distribution:
      recall: 0.2
      comprehension: 0.3
      application: 0.25
      analysis: 0.15
      synthesis: 0.08
      evaluation: 0.02
    
    # Two-axis control
    depth_weights:  # How many cards at each depth
      0: 1.0  # Root
      1: 0.8  # Chapter
      2: 1.0  # Concept  
      3: 0.6  # Detail
    
  # Critic configuration
  critic:
    selection_strategy: "balanced"  # balanced, strict, lenient
    diversity_weight: 0.3  # How much to favor diverse difficulties
    
  # Learning goals
  learning_goals:
    mastery_level: "comprehensive"  # basic, intermediate, comprehensive, expert
    focus_areas:
      - "conceptual_understanding"
      - "problem_solving"
      - "theoretical_foundations"
      - "practical_applications"
    time_frame: "semester"  # affects card density
    
  # Quality assurance
  quality:
    verify_answers: true
    refine_cards: true
    max_refine_iterations: 3
    confidence_threshold: 0.8
```

## Benefits and Use Cases

### Educational Advantages

1. **Hierarchical Learning**: Students progress from high-level understanding to detailed mastery
2. **Prerequisite Tracking**: Cards indicate what concepts should be learned first
3. **Adaptive Difficulty**: Cards match student's current level
4. **Complete Coverage**: Ensures all important concepts are covered
5. **Relationship Understanding**: Cards test connections between concepts

### Use Case Examples

1. **Mathematics Textbook**
   - Root: "Linear Algebra Fundamentals"
   - Chapters: "Vector Spaces", "Linear Transformations", "Eigenvalues"
   - Concepts: "Basis", "Dimension", "Kernel"
   - Details: Specific theorems, proofs, computational methods

2. **Research Paper**
   - Root: Paper summary and contributions
   - Sections: Background, Methods, Results
   - Concepts: Key algorithms, theoretical results
   - Details: Specific equations, experimental setup

3. **Programming Course**
   - Root: "Data Structures and Algorithms"
   - Chapters: "Sorting", "Trees", "Graphs"
   - Concepts: "Binary Search Tree", "Graph Traversal"
   - Details: Implementation details, complexity analysis

### Integration with Existing Swanki

```python
# In main pipeline.py
def select_processing_strategy(config, document_analysis):
    """Select between sliding window and DAG decomposition"""
    
    if config.processing.strategy == "dag_decomposition":
        return DAGProcessingPipeline(config)
    elif config.processing.strategy == "adaptive":
        # Auto-detect best strategy
        if document_analysis.has_hierarchy and document_analysis.concept_density > 0.7:
            return DAGProcessingPipeline(config)
        else:
            return SlidingWindowPipeline(config)
    else:
        return SlidingWindowPipeline(config)
```

## Future Enhancements

1. **Multi-Document DAGs**: Connect concepts across multiple documents
2. **Collaborative Filtering**: Learn from user performance to improve card selection
3. **Dynamic Difficulty Adjustment**: Adapt card difficulty based on user performance
4. **Concept Map Visualization**: Generate visual representation of knowledge graph
5. **Spaced Repetition Integration**: Schedule cards based on DAG structure and prerequisites

This DAG-based approach transforms Swanki from a linear document processor into an intelligent learning system that understands and teaches the hierarchical structure of knowledge.