from manim import *
from collections import defaultdict

def arrange_points_from_center_X(center, space, n_points):
    """Arrange Points in rectangular Line from a center point. with n_points"""
    points = np.zeros((n_points, 3))
    points[:, 1:] = center[1:]  # Keep y and z constant
    points[:, 0] = np.linspace(-space * (n_points-1)/2, space * (n_points-1)/2, n_points)  # Spread points along x-axis
    print(f"Arranged points: {points}")
    points += center
    return points

def arrange_points_from_center_grid(center, space, n, m):
    """Arrange Points in rectangular Line from a center point. with n_points"""
    points = np.zeros((n, m, 3))
    for i in range(n):
        points[i, :, 0] = np.linspace(-space * (m-1)/2, space * (m-1)/2, m)  # Spread points along x-axis
    for i in range(m):
        points[:, i, 1] = np.linspace(-space * (n-1)/2, space * (n-1)/2, n)  # Spread points along x-axis
    print(f"Arranged points: {points}")
    points += center
    points = points.reshape(n * m, 3)  # Flatten to 2D array
    return points

class ProteinEvolutionAnimation(Scene):
    def construct(self):
        # Scene 1: Title and Introduction
        self.scene_1_title()
        
        # Scene 2: Original sequence
        self.scene_2_original_sequence()
        
        # Scene 3: Query and find related sequences
        self.scene_3_evolutionary_ancestry()
        
        # Scene 4: Show MSA formation
        self.scene_4_msa_formation()
        
        # Scene 5: Highlight insights
        self.scene_5_insights()

    def scene_1_title(self):
        """Scene 1: The Origin - Title introduction"""
        title = Text("How Models Capture Evolutionary History", font_size=48)
        title.set_color(BLUE)
        
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

    def scene_2_original_sequence(self):
        """Scene 2: Show the original sequence with typing effect"""
        # Header text
        header = Text("First, we start with an amino acid sequence", font_size=36)
        header.set_color(BLUE)
        header.to_edge(UP)
        
        self.play(Write(header))
        
        # Original sequence - appears letter by letter
        query_seq = "ACKERGWGMWPGWMPMPO"
        seq_label = Text("Seq: ", font_size=40)
        seq_label.set_color(WHITE)
        
        # Create individual letters for typing effect
        letters = []
        for i, letter in enumerate(query_seq):
            letter_text = Text(letter, font_size=40)
            letter_text.set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
            letters.append(letter_text)
        
        # Position the sequence
        seq_group = VGroup(seq_label, *letters)
        seq_group.arrange(RIGHT, buff=0.1)
        seq_group.move_to(ORIGIN)
        
        # Animate sequence appearance
        self.play(Write(seq_label))
        for letter in letters:
            self.play(Write(letter), run_time=0.1)
        
        self.wait(1)
        
        # Store for later use
        self.original_seq = seq_group
        self.header = header

    def scene_3_evolutionary_ancestry(self):
        """Scene 3: Query database and show related sequences"""
        # Move original sequence up
        self.play(
            self.original_seq.animate.to_edge(UP, buff=1.5),
            FadeOut(self.header)
        )
        
        # Database query animation
        query_text = Text("Querying evolutionary databases...", font_size=32)
        query_text.set_color(BLUE)
        query_text.move_to(ORIGIN + UP)
        
        self.play(Write(query_text))
        
        # Simulate database search with rotating dots
        dots = VGroup(*[Dot().shift(i*0.3*RIGHT) for i in range(3)])
        dots.next_to(query_text, RIGHT)
        
        self.play(Create(dots))
        self.play(dots.animate.rotate(PI), run_time=2)
        self.play(FadeOut(query_text), FadeOut(dots))
        
        # Show related sequences with highlighted differences
        related_seqs = [
            ("ACKERGWGLWPGWMPMPO", [9]),   # L instead of M at position 9
            ("ACKERGWGMWPGWMPMPQ", [17]),  # Q instead of O at position 17
            ("ACKERGWRMWPGWMPMPO", [7]),   # R instead of G at position 7
            ("ACKERGWRMWPGWLPMPQ", [7, 14, 17])  # Multiple changes
        ]
        
        self.related_sequences = []
        
        for i, (seq, diff_positions) in enumerate(related_seqs):
            # Create sequence with highlighting
            seq_text = self.create_highlighted_sequence(seq, diff_positions)
            
            # Position below previous sequence
            if i == 0:
                seq_text.next_to(self.original_seq, DOWN, buff=0.8)
            else:
                seq_text.next_to(self.related_sequences[-1], DOWN, buff=0.3)
            
            self.related_sequences.append(seq_text)
            self.play(Write(seq_text), run_time=1)
            self.wait(0.5)

    def create_highlighted_sequence(self, sequence, highlight_positions):
        """Create a sequence with specific positions highlighted in red"""
        seq_label = Text("Seq: ", font_size=32)
        seq_label.set_color(WHITE)
        
        letters = []
        for i, letter in enumerate(sequence):
            letter_text = Text(letter, font_size=32)
            if i in highlight_positions:
                letter_text.set_color(RED)
            else:
                letter_text.set_color(WHITE)
            letters.append(letter_text)
        
        seq_group = VGroup(seq_label, *letters)
        seq_group.arrange(RIGHT, buff=0.05)
        
        return seq_group

    def scene_4_msa_formation(self):
        """Scene 4: Form MSA stack"""
        # Title for MSA
        msa_title = Text("Multiple Sequence Alignment (MSA)", font_size=36)
        msa_title.set_color(BLUE)
        msa_title.to_edge(UP)
        
        self.play(Write(msa_title))
        
        # Collect all sequences
        all_sequences = [self.original_seq] + self.related_sequences
        
        # Create MSA grid representation
        msa_grid = self.create_msa_grid()
        msa_grid.move_to(ORIGIN)
        
        # Transform sequences into grid
        self.play(
            *[FadeOut(seq) for seq in all_sequences],
            FadeIn(msa_grid),
            run_time=2
        )
        
        self.wait(1)
        self.msa_grid = msa_grid
        self.msa_title = msa_title

    def create_msa_grid(self):
        """Create a visual representation of MSA as a grid"""
        # Create a 5x18 grid (5 sequences, 18 positions)
        sequences = [
            "ACKERGWGMWPGWMPMPO",  # original
            "ACKERGWGLWPGWMPMPO",  # L->M
            "ACKERGWGMWPGWMPMPQ",  # O->Q
            "ACKERGWRMWPGWMPMPO",  # G->R
            "ACKERGWRMWPGWLPMPQ"   # multiple
        ]
        
        grid = VGroup()
        
        for row, seq in enumerate(sequences):
            for col, letter in enumerate(seq):
                # Create rectangle for each position
                rect = Rectangle(width=0.4, height=0.4)
                
                # Color based on conservation
                if self.is_conserved_position(col, sequences):
                    rect.set_fill(GREEN, opacity=0.7)
                    rect.set_stroke(GREEN)
                else:
                    rect.set_fill(RED, opacity=0.3)
                    rect.set_stroke(RED)
                
                # Add letter
                letter_text = Text(letter, font_size=16)
                letter_text.move_to(rect.get_center())
                
                # Position in grid
                rect.shift(col * 0.5 * RIGHT + row * 0.5 * DOWN)
                letter_text.shift(col * 0.5 * RIGHT + row * 0.5 * DOWN)
                
                grid.add(rect, letter_text)
        
        return grid

    def is_conserved_position(self, position, sequences):
        """Check if a position is conserved across sequences"""
        letters = [seq[position] for seq in sequences]
        return len(set(letters)) == 1

    def scene_5_insights(self):
        """Scene 5: Highlight the insights"""
        # Add insight text
        insight_text = Text(
            "Models learn from this pattern:\n"
            "• Green = Conserved (important for structure)\n"
            "• Red = Variable (flexible regions)",
            font_size=28
        )
        insight_text.set_color(WHITE)
        insight_text.to_edge(DOWN)
        
        self.play(Write(insight_text))
        
        # Highlight conserved vs variable columns with animations
        self.play(self.msa_grid.animate.scale(1.2))
        
        # Add arrows pointing to different regions
        conserved_arrow = Arrow(
            start=ORIGIN + 2*LEFT + 0.5*UP,
            end=ORIGIN + 1.5*LEFT,
            color=GREEN
        )
        variable_arrow = Arrow(
            start=ORIGIN + 2*RIGHT + 0.5*UP,
            end=ORIGIN + 1.5*RIGHT,
            color=RED
        )
        
        conserved_label = Text("Conserved", font_size=20, color=GREEN)
        conserved_label.next_to(conserved_arrow, UP)
        
        variable_label = Text("Variable", font_size=20, color=RED)
        variable_label.next_to(variable_arrow, UP)
        
        self.play(
            Create(conserved_arrow),
            Create(variable_arrow),
            Write(conserved_label),
            Write(variable_label)
        )
        
        self.wait(3)
        
        # Final message
        final_text = Text(
            "This evolutionary information helps  models \n"
            "predict protein structure and function!",
            font_size=32,
            color=BLUE
        )
        final_text.move_to(ORIGIN + 2*DOWN)
        
        self.play(
            FadeOut(insight_text),
            Write(final_text)
        )
        
        self.wait(3)