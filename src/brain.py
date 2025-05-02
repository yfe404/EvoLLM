import random
import numpy as np

N_SENSORY_NEURONS = 8
N_INTERNAL_NEURONS = 4
N_ACTION_NEURONS = 5

N_CONNECTIONS = 10

def softmax(x):
    f_x = np.exp(x) / np.sum(np.exp(x))
    return f_x

def generate_random_gene():
    return "".join(random.choices("0123456789abcdef", k=8))
    

# Generate a random genome and random values for the sensory neurons
sensory_neurons = np.random.uniform(-1, 1, N_SENSORY_NEURONS)
genome = [generate_random_gene() for _ in range(N_CONNECTIONS)]
print(genome)

internal_neurons = [0 for _ in range(N_INTERNAL_NEURONS)]
action_neurons = [0 for _ in range(N_ACTION_NEURONS)]


# @todo: need to check the order of processing for internal to internal
stack_internal_to_action = []
stack_internal_to_internal = []

for gene in genome:
    bin_gene = format(int(gene, 16), "032b")
 
    source_type = int(bin_gene[0], 2) # 0: from input sensory neuron, 1: from internal neuron
    if source_type == 0:
        source_id = int(bin_gene[1:8], 2) % N_SENSORY_NEURONS
    elif source_type == 1:
        source_id = int(bin_gene[1:8], 2) % N_INTERNAL_NEURONS

    sink_type = int(bin_gene[8], 2) # 0: to internal neuron, 1: to action neuron
    if sink_type == 0:
        sink_id = int(bin_gene[9:16], 2) % N_INTERNAL_NEURONS
    elif sink_type == 1:
        sink_id = int(bin_gene[9:16], 2) % N_ACTION_NEURONS

    weight = (int(bin_gene[16:], 2) - 32768) / 8192 # -4.0 .. 4.0

#    print(source_type, sink_type, source_id, sink_id, weight)
        
    if source_type == 1 and sink_type == 0:
        stack_internal_to_internal.append((source_id, sink_id, weight))
    elif source_type == 1 and sink_type == 1:
        stack_internal_to_action.append((source_id, sink_id, weight))

    else:
        # sensory -> internal
        if source_type == 0 and sink_type == 0:
            internal_neurons[sink_id] += weight * sensory_neurons[source_id]
        # sensory -> action
        elif source_type == 0 and sink_type == 1:
            action_neurons[sink_id] += weight * sensory_neurons[source_id]

for (source_id, sink_id, weight) in stack_internal_to_internal:
    internal_neurons[sink_id] += weight * internal_neurons[source_id]

internal_neurons = np.tanh(internal_neurons)

for (source_id, sink_id, weight) in stack_internal_to_action:
    action_neurons[sink_id] += weight * internal_neurons[source_id]

action_neurons = np.tanh(action_neurons)


print(sensory_neurons)
print(internal_neurons)
print(action_neurons)
print(softmax(action_neurons))

action = np.random.choice(range(len(action_neurons)), p=softmax(action_neurons))

print(action)


print("+++++++++++++++++++++")
