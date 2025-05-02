from brain import generate_random_gene
from brain_viz import visualize_brain

def main():
    genome = [generate_random_gene() for _ in range(10)]
    visualize_brain(genome)

if __name__ == '__main__':
    main()
