import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import random

class AminoAcidFolder:
    def __init__(self, n_residues=200):
        self.n_residues = n_residues
        self.frames = 50 # 8 seconds at 30 fps
        
        # Generate initial extended chain
        self.initial_positions = self.generate_extended_chain()
        self.final_positions = self.generate_folded_structure_from_pdb()
        
        # Color scheme for different atom types
        self.atom_colors = {
            'C': '#404040',  # Carbon - dark gray
            'N': '#1E90FF',  # Nitrogen - dodger blue
            'O': '#FF4500',  # Oxygen - orange red
            'H': '#F5F5F5',  # Hydrogen - white smoke
            'S': '#FFD700'   # Sulfur - gold
        }
        
        # Generate atom types for each residue
        self.atom_types = self.generate_atom_types()
        
    def generate_extended_chain(self):
        """Generate an extended amino acid chain"""
        positions = []
        for i in range(self.n_residues):
            # Extended chain along x-axis with slight random variations
            x = i * 3.8  # Typical peptide bond length
            y = 0
            z = 0
            positions.append([x, y, z])
        return np.array(positions)
    
    def generate_folded_structure(self):
        """Generate a folded protein-like structure"""
        positions = []
        center = np.array([self.n_residues * 1.9, 0, 0])  # Center of folded structure
        
        for i in range(self.n_residues):
            # Create a more realistic folded structure
            theta = i * 2 * np.pi / self.n_residues * 3  # Multiple turns
            phi = np.sin(i * 0.5) * np.pi / 4  # Variation in phi angle
            
            # Spherical coordinates with some randomness
            r = 8 + 3 * np.sin(i * 0.3)  # Varying radius
            x = center[0] + r * np.cos(theta) * np.cos(phi)
            y = center[1] + r * np.sin(theta) * np.cos(phi)
            z = center[2] + r * np.sin(phi)
            
            positions.append([x, y, z])
        
        return np.array(positions)
    
    def generate_folded_structure_from_pdb(self):
        """Generate a folded protein-like structure"""
        
        with open('/Users/adityadude/Documents/Python/ProteinFolding/output/Vritti_InsulinChainB/test_340ad_unrelaxed_rank_003_alphafold2_ptm_model_1_seed_000.pdb', 'r') as f:
            lines = f.readlines()
            positions = np.zeros((len(lines), 3))
            for i, line in enumerate(lines):
                if line.startswith('ATOM'):
                    parts = line.split()
                    x = float(parts[6])
                    y = float(parts[7])
                    z = float(parts[8])
                    positions[i] = [x, y, z]
            print(positions.shape)
        return positions[:: positions.shape[0] // self.n_residues][:self.n_residues]
    
    def generate_atom_types(self):
        """Generate atom types for each residue"""
        atom_types = []
        for i in range(self.n_residues):
            # Simplified: backbone atoms plus side chain
            if i % 4 == 0:
                atom_types.append('N')
            elif i % 4 == 1:
                atom_types.append('C')
            elif i % 4 == 2:
                atom_types.append('O')
            else:
                atom_types.append('S' if random.random() > 0.8 else 'C')
        return atom_types
    
    def interpolate_positions(self, frame):
        """Interpolate between initial and final positions"""
        # Use smooth easing function
        t = frame / (self.frames - 1)
        # Ease-in-out cubic function for smooth animation
        t = 3 * t**2 - 2 * t**3 if t < 0.5 else 1 - 3 * (1-t)**2 + 2 * (1-t)**3
        
        return (1-t) * self.initial_positions + t * self.final_positions
    def set_axes_equal(ax):
        '''Sets equal aspect ratio for a 3D plot'''
        limits = np.array([
            ax.get_xlim3d(),
            ax.get_ylim3d(),
            ax.get_zlim3d(),
        ])
        spans = limits[:, 1] - limits[:, 0]
        centers = np.mean(limits, axis=1)
        max_span = max(spans)
    
        for center, axis in zip(centers, ['x', 'y', 'z']):
            getattr(ax, f'set_{axis}lim')(center - max_span/2, center + max_span/2)

    def create_animation(self):
        """Create the folding animation"""
        # Set up the figure with dark theme
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        # Enhanced aesthetics
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        
        # Remove axes for cleaner look
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.grid(False)
        
        # Hide axes
        ax.set_axis_off()
        
        def animate(frame):
            ax.clear()
            ax.set_facecolor('black')
            ax.set_axis_off()
            
            # Get current positions
            current_positions = self.interpolate_positions(frame)
            
            # Plot bonds as lines with gradient effect
            for i in range(len(current_positions) - 1):
                x_coords = [current_positions[i][0], current_positions[i+1][0]]
                y_coords = [current_positions[i][1], current_positions[i+1][1]]
                z_coords = [current_positions[i][2], current_positions[i+1][2]]
                
                # Gradient bond color based on position in chain
                bond_color = plt.cm.plasma(i / len(current_positions))
                ax.plot(x_coords, y_coords, z_coords, 
                       color=bond_color, linewidth=2.5, alpha=0.8)
            
            # Plot atoms as spheres with different sizes and colors
            for i, (pos, atom_type) in enumerate(zip(current_positions, self.atom_types)):
                color = self.atom_colors[atom_type]
                size = 150 if atom_type in ['C', 'N', 'O', 'S'] else 80
                
                # Add glow effect with multiple layers
                ax.scatter(pos[0], pos[1], pos[2], 
                          c=color, s=size*1.5, alpha=0.3, edgecolors='none')
                ax.scatter(pos[0], pos[1], pos[2], 
                          c=color, s=size, alpha=0.8, edgecolors='white', linewidth=0.5)
            
            # Dynamic camera rotation
            angle = frame * 360 / self.frames
            ax.view_init(elev=20 + 10*np.sin(frame*0.02), azim=angle)
            
            # Set limits to keep protein centered
            all_positions = np.vstack([self.initial_positions, self.final_positions])
            margin = 5
            ax.set_xlim(all_positions[:, 0].min() - margin, all_positions[:, 0].max() + margin)
            ax.set_ylim(all_positions[:, 1].min() - margin, all_positions[:, 1].max() + margin)
            # ax.set_zlim(all_positions[:, 2].min() - margin, all_positions[:, 2].max() + margin)

            # Add title with progress
            progress = frame / (self.frames - 1) * 100
            ax.text2D(0.02, 0.95, f'Protein Folding Animation\nProgress: {progress:.1f}%', 
                     transform=ax.transAxes, fontsize=12, color='white', 
                     bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
            
            # Add atom legend
            legend_text = "Atom Types:\n"
            legend_text += "● Carbon (C)\n● Nitrogen (N)\n● Oxygen (O)\n● Sulfur (S)"
            ax.text2D(0.02, 0.02, legend_text, transform=ax.transAxes, 
                     fontsize=10, color='white',
                     bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=self.frames, 
                                     interval=1000/60, blit=False, repeat=False)
        
        return fig, anim

def main():
    # Create the amino acid folder
    folder = AminoAcidFolder(n_residues=200)  # 25 residues for more complex structure
    # folder.generate_folded_structure_from_pdb()  # Load folded structure from PDB
    # Create and display animation
    fig, anim = folder.create_animation()
    
    # Show the animation
    plt.tight_layout()
    plt.show()
    
    # Uncomment to save as MP4 (requires ffmpeg)
    # anim.save('amino_acid_folding.mp4', writer='ffmpeg', fps=30, dpi=150)
    
    # Uncomment to save as GIF
    # anim.save('amino_acid_folding.gif', writer='pillow', fps=30, dpi=150)

if __name__ == "__main__":
    main()