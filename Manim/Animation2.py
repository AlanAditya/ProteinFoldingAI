from manim import *
import numpy as np
def arrange_points_from_center_X(center, space, n_points):
    """Arrange Points in rectangular Line from a center point. with n_points"""
    points = np.zeros((n_points, 3))
    points[:, 0] = np.linspace(-space * (n_points-1)/2, space * (n_points-1)/2, n_points)  # Spread points along x-axis
    print(f"Arranged points: {points}")
    points += center
    return points

def arrange_points_from_center_Y(center, space, n_points):
    """Arrange Points in rectangular Line from a center point. with n_points"""
    points = np.zeros((n_points, 3))
    points[:, 1] = np.linspace(-space * (n_points-1)/2, space * (n_points-1)/2, n_points)  # Spread points along x-axis
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

class ProteinPairwiseRepresentation(Scene):
    def construct(self):
        # Scene 1: Laying Out the Sequence
        self.scene_1_sequence_layout()
        self.wait(2)
        self.clear()
        
        # Scene 2: Forming the Pairwise Grid
        self.scene_2_pairwise_grid()
        self.wait(2)
        
        # Scene 3: Showing Why the Diagonal is Bright
        self.scene_3_diagonal_explanation()
        self.wait(2)
        
        # Scene 4: Folding the Protein
        self.scene_4_protein_folding()
        self.wait(2)
        
        # Scene 5: New Contacts Appear in the Grid
        self.scene_5_new_contacts()
        self.wait(2)
        
        # Scene 6: Mapping I and J to the Structure
        self.scene_6_mapping_contacts()
        self.wait(2)
        
        # Scene 7: Final Summary
        self.scene_7_summary()
        self.wait(3)

    def scene_1_sequence_layout(self):
        """Scene 1: Laying Out the Sequence"""
        title = Text("Understanding Pairwise Representation in Proteins", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create horizontal sequence
        amino_acids_h = VGroup()
        positionX = arrange_points_from_center_X(center=ORIGIN, space=0.6, n_points=10)
        for i in range(10):
            circle = Circle(radius=0.2, color=BLUE, fill_opacity=0.7)
            label = Text(f"A{i+1}", font_size=20, color=WHITE)
            aa = VGroup(circle, label)
            aa.move_to(positionX[i] + UP * 2.5)
            amino_acids_h.add(aa)
        
        # Create vertical sequence
        amino_acids_v = VGroup()
        positionY = arrange_points_from_center_Y(center=ORIGIN, space=0.6, n_points=10)
        for i in range(10):
            circle = Circle(radius=0.2, color=BLUE, fill_opacity=0.7)
            label = Text(f"A{i+1}", font_size=20, color=WHITE)
            aa = VGroup(circle, label)
            aa.move_to(LEFT * 3 + positionY[i])
            amino_acids_v.add(aa)
        
        # Annotations
        h_label = Text("Horizontal Sequence", font_size=24, color=YELLOW)
        h_label.next_to(amino_acids_h, DOWN, buff=0.5)
        
        v_label = Text("Vertical\nSequence", font_size=24, color=YELLOW)
        v_label.next_to(amino_acids_v, LEFT, buff=0.5)
        
        self.play(
            FadeIn(amino_acids_h),
            FadeIn(amino_acids_v),
            Write(h_label),
            Write(v_label)
        )
        
        voiceover = Text(
            "We begin with a protein — a sequence of amino acids.\nFor simplicity, we use just ten.",
            font_size=20, color=WHITE
        ).to_edge(DOWN)
        self.play(Write(voiceover))

    def scene_2_pairwise_grid(self):
        """Scene 2: Forming the Pairwise Grid"""
        # Create the grid
        grid = VGroup()
        cells = []
        
        for i in range(10):
            row = []
            for j in range(10):
                cell = Square(side_length=0.4, color=WHITE, stroke_width=1)
                cell.move_to(RIGHT * (j - 4.5) * 0.4 + DOWN * (i - 4.5) * 0.4)
                
                # Diagonal cells are bright
                if abs(i - j) <= 1:  # Diagonal and adjacent
                    cell.set_fill(YELLOW, opacity=0.8)
                else:
                    cell.set_fill(GRAY, opacity=0.2)
                
                grid.add(cell)
                row.append(cell)
            cells.append(row)
        
        # Add amino acid labels
        h_labels = VGroup()
        v_labels = VGroup()
        
        for i in range(10):
            h_label = Text(f"A{i+1}", font_size=16, color=BLUE)
            h_label.move_to(RIGHT * (i - 4.5) * 0.4 + UP * 2.5)
            h_labels.add(h_label)
            
            v_label = Text(f"A{i+1}", font_size=16, color=BLUE)
            v_label.move_to(LEFT * 2.5 + DOWN * (i - 4.5) * 0.4)
            v_labels.add(v_label)
        
        title = Text("Pairwise Matrix Formation", font_size=32, color=WHITE)
        title.to_edge(UP)
        
        self.play(
            Write(title),
            FadeIn(grid),
            FadeIn(h_labels),
            FadeIn(v_labels)
        )
        
        explanation = Text(
            "Each cell represents the relationship between two amino acids.\nDiagonal cells show local interactions.",
            font_size=18, color=WHITE
        ).to_edge(DOWN)
        
        self.play(Write(explanation))
        
        # Store for later use
        self.grid = grid
        self.cells = cells
        self.h_labels = h_labels
        self.v_labels = v_labels

    def scene_3_diagonal_explanation(self):
        """Scene 3: Showing Why the Diagonal is Bright"""
        # Create linear chain
        chain = VGroup()
        chain_circles = []
        
        for i in range(10):
            circle = Circle(radius=0.25, color=BLUE, fill_opacity=0.7)
            label = Text(f"A{i+1}", font_size=16, color=WHITE)
            aa = VGroup(circle, label)
            aa.move_to(RIGHT * (i - 4.5) * 0.6 + UP * 2)
            chain.add(aa)
            chain_circles.append(circle)
        
        # Connect adjacent amino acids
        connections = VGroup()
        for i in range(9):
            line = Line(
                chain_circles[i].get_center(),
                chain_circles[i+1].get_center(),
                color=RED, stroke_width=3
            )
            connections.add(line)
        
        self.play(
            FadeIn(chain),
            Create(connections)
        )
        
        # Pulse corresponding diagonal cells
        diagonal_cells = []
        for i in range(9):
            diagonal_cells.append(self.cells[i][i+1])
            diagonal_cells.append(self.cells[i+1][i])
        
        self.play(
            *[cell.animate.set_fill(RED, opacity=1.0) for cell in diagonal_cells]
        )
        
        explanation = Text(
            "In a straight chain, amino acids only interact with neighbors — diagonal dominates.",
            font_size=18, color=WHITE
        ).to_edge(DOWN)
        
        self.play(Write(explanation))

    def scene_4_protein_folding(self):
        """Scene 4: Folding the Protein"""
        # Define folded positions (creating a compact structure)
        folded_positions = [
            UP * 1.5 + LEFT * 1,      # A1
            UP * 1.5,                 # A2
            UP * 1.5 + RIGHT * 1,     # A3
            UP * 0.5 + RIGHT * 1,     # A4
            DOWN * 0.5 + RIGHT * 1,   # A5
            DOWN * 1.5 + RIGHT * 1,   # A6
            DOWN * 1.5,               # A7
            DOWN * 1.5 + LEFT * 1,    # A8
            DOWN * 0.5 + LEFT * 1,    # A9
            UP * 0.5 + LEFT * 1       # A10
        ]
        
        # Create folded protein
        folded_chain = VGroup()
        folded_circles = []
        
        for i, pos in enumerate(folded_positions):
            circle = Circle(radius=0.25, color=BLUE, fill_opacity=0.7)
            label = Text(f"A{i+1}", font_size=16, color=WHITE)
            aa = VGroup(circle, label)
            aa.move_to(pos + RIGHT * 3)
            folded_chain.add(aa)
            folded_circles.append(circle)
        
        # Connect the backbone
        backbone = VGroup()
        for i in range(9):
            line = Line(
                folded_circles[i].get_center(),
                folded_circles[i+1].get_center(),
                color=GREEN, stroke_width=2
            )
            backbone.add(line)
        
        title = Text("Protein Folding", font_size=32, color=WHITE)
        title.to_edge(UP)
        
        self.play(
            Transform(self.grid.copy(), title),
            FadeIn(folded_chain),
            Create(backbone)
        )
        
        explanation = Text(
            "Proteins fold, bringing distant parts of the chain close together in 3D space.",
            font_size=18, color=WHITE
        ).to_edge(DOWN)
        
        self.play(Write(explanation))
        
        # Store for later use
        self.folded_circles = folded_circles

    def scene_5_new_contacts(self):
        """Scene 5: New Contacts Appear in the Grid"""
        # Define new contacts based on folded structure (distance threshold)
        new_contacts = []
        contact_lines = VGroup()
        
        # Calculate distances and find new contacts
        for i in range(10):
            for j in range(i+2, 10):  # Skip adjacent residues
                pos_i = self.folded_circles[i].get_center()
                pos_j = self.folded_circles[j].get_center()
                distance = np.linalg.norm(pos_i - pos_j)
                
                if distance < 1.2:  # Contact threshold
                    new_contacts.append((i, j))
                    line = Line(pos_i, pos_j, color=RED, stroke_width=2)
                    contact_lines.add(line)
        
        # Light up corresponding cells in the matrix
        new_contact_cells = []
        for i, j in new_contacts:
            new_contact_cells.append(self.cells[i][j])
            new_contact_cells.append(self.cells[j][i])
        
        self.play(Create(contact_lines))
        
        self.play(
            *[cell.animate.set_fill(ORANGE, opacity=0.9) for cell in new_contact_cells]
        )
        
        explanation = Text(
            "New contacts appear! Amino acids far in sequence are now close in space.",
            font_size=18, color=WHITE
        ).to_edge(DOWN)
        
        self.play(Write(explanation))

    def scene_6_mapping_contacts(self):
        """Scene 6: Mapping I and J to the Structure"""
        # Highlight a specific contact
        i, j = 2, 7  # A3 and A8
        
        # Highlight cells
        cell_ij = self.cells[i][j]
        cell_ji = self.cells[j][i]
        
        # Highlight amino acids
        aa_i = self.folded_circles[i]
        aa_j = self.folded_circles[j]
        
        # Create connection line
        contact_line = Line(
            aa_i.get_center(), aa_j.get_center(),
            color=YELLOW, stroke_width=4
        )
        
        # Coordinate labels
        coord_label = Text(f"(i={i+1}, j={j+1})", font_size=24, color=YELLOW)
        coord_label.move_to(UP * 3 + RIGHT * 2)
        
        self.play(
            cell_ij.animate.set_fill(YELLOW, opacity=1.0),
            cell_ji.animate.set_fill(YELLOW, opacity=1.0),
            aa_i.animate.set_color(YELLOW),
            aa_j.animate.set_color(YELLOW),
            Create(contact_line),
            Write(coord_label)
        )
        
        mapping_text = Text(
            "(i, j) → Spatial Contact", font_size=20, color=YELLOW
        ).move_to(DOWN * 2.5)
        
        self.play(Write(mapping_text))

    def scene_7_summary(self):
        """Scene 7: Final Summary"""
        # Create a clean summary view
        summary_title = Text(
            "Pairwise Representation: From 1D Sequence to 2D Contact Map",
            font_size=28, color=WHITE
        )
        summary_title.to_edge(UP)
        
        # Small folded protein
        mini_protein = VGroup()
        for i in range(5):
            circle = Circle(radius=0.15, color=BLUE, fill_opacity=0.7)
            circle.move_to(LEFT * 4 + UP * 0.5 + RIGHT * i * 0.3)
            mini_protein.add(circle)
        
        # Small contact matrix
        mini_matrix = VGroup()
        for i in range(5):
            for j in range(5):
                cell = Square(side_length=0.25, color=WHITE, stroke_width=1)
                cell.move_to(RIGHT * 3 + RIGHT * j * 0.25 + DOWN * i * 0.25)
                if i == j or abs(i-j) == 1:
                    cell.set_fill(YELLOW, opacity=0.7)
                elif (i, j) in [(0, 3), (1, 4), (3, 0), (4, 1)]:
                    cell.set_fill(ORANGE, opacity=0.7)
                else:
                    cell.set_fill(GRAY, opacity=0.2)
                mini_matrix.add(cell)
        
        protein_label = Text("Folded Protein", font_size=16, color=BLUE)
        protein_label.next_to(mini_protein, DOWN)
        
        matrix_label = Text("Contact Map", font_size=16, color=ORANGE)
        matrix_label.next_to(mini_matrix, DOWN)
        
        final_explanation = Text(
            "This pairwise representation forms the foundation for predicting protein structure —\nfrom a 1D sequence to a 2D map of spatial relationships.",
            font_size=18, color=WHITE
        ).to_edge(DOWN)
        
        self.play(
            Write(summary_title),
            FadeIn(mini_protein),
            FadeIn(mini_matrix),
            Write(protein_label),
            Write(matrix_label),
            Write(final_explanation)
        )
        
        # Final flourish - arrow connecting them
        arrow = Arrow(
            mini_protein.get_right() + RIGHT * 0.3,
            mini_matrix.get_left() + LEFT * 0.3,
            color=GREEN, stroke_width=3
        )
        
        self.play(Create(arrow))

# To render this scene, use:
# manim -pql protein_pairwise_manim.py ProteinPairwiseRepresentation