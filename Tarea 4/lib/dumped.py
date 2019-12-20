"""
This module contains pieces of code we dumped, because of their inefficiency and because we could
find better solutions:
"""


"""
easy_shaders.py:

def StateToGPUShape(state):
    assert isinstance(state, interpol.State)

    vertexData = np.array(state.vertex_data, dtype=np.float32)
    indices = np.array(state.index_data, dtype=np.uint32)

    # Here the new shape will be stored
    gpuShape = GPUShape()

    gpuShape.size = len(state.index_data)
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)
    gpuShape.index_data = indices
    gpuShape.vertex_data = vertexData
    gpuShape.n_of_vertex = indices.max()

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape
"""

"""
States were not needed anymore, since we used another way.
This method was supposed to make interpolations using the xyz coordinates. It would have worked,
but a lot of work and definitions were needed, such as bones and to store every node.
Interpolations:
class State:
    def __init__(self):
        self.vertex_data = []
        self.index_data = []

    # Creates a new state, which is the difference between two states
    def __sub__(self, other, num_of_ver):
        if isinstance(other, State) or (other.index_data.len() != self.index_data.len()):
            new_state = State()
            new_state.index_data = self.index_data
            new_vertex_data = []
            for ver in range(num_of_ver):  # these ones should be the same as the other state index data
                # Assuming just colors and xyz position.
                new_vertex_data += [other.vertex_data[ver * 6] - self.vertex_data[ver * 6],    # x coordinate
                                    other.vertex_data[ver * 6 + 1] - self.vertex_data[ver * 6 + 1],  # y coordinate
                                    other.vertex_data[ver * 6 + 2] - self.vertex_data[ver * 6 + 2],  # z coordinate
                                    ]
            new_state.vertex_data = new_vertex_data
            return new_state

        else:
            raise Exception("Two states of the same object needed")
            return None


def interpol(first_state, second_state, intermediate_frames, function_type="linear"):
    Makes an interpolation between the First and Second States using the given method.

    if function_type == "linear":
        for t in range(0, 1, intermediate_frames + 1):
            state = first_state * (1 - t) + second_state * t
            es.StateToGPUShape(state)

    elif function_type == "spline":
        vertex = [first_state.vertex, second_state.vertex]
        intermediate_curve = cr.getSpline(vertex, intermediate_frames)


    elif function_type == "sine":
        for angle in range(0, np.pi / 2, intermediate_frames + 1):
            state = first_state * np.sin(angle) + second_state * np.sin(angle + np.pi / 2)
            es.StateToGPUShape(state)

    else:
        raise Exception("Invalid interpolation method")
"""