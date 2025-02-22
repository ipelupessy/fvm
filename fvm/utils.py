import numpy

from scipy import integrate

def create_state_mtx(state, nx, ny, nz, dof):
    state_mtx = numpy.zeros([nx, ny, nz, dof])
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                for d in range(dof):
                    state_mtx[i, j, k, d] = state[d + i * dof + j * dof * nx + k * dof * nx * ny]
    return state_mtx

def create_state_vec(state_mtx, nx, ny, nz, dof):
    state = numpy.zeros(nx * ny * nz * dof)

    row = 0
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                for d in range(dof):
                    state[row] = state_mtx[i, j, k, d]
                    row += 1
    return state

def create_uniform_coordinate_vector(start, end, nx):
    dx = (end - start) / nx
    return numpy.roll(numpy.arange(start - dx, end + 2 * dx, dx), -2)

def create_stretched_coordinate_vector(start, end, nx, sigma):
    if start < 0 or end > 1:
        raise ValueError('Grid stretching currently only works for a [0, 1] domain')

    x = create_uniform_coordinate_vector(start, end, nx)
    return 0.5 * (1 + numpy.tanh(2 * sigma * (x - 0.5)) / numpy.tanh(sigma))

def compute_streamfunction(u, v, x, y):
    x, y = numpy.meshgrid(x, y)

    psiv = integrate.cumtrapz(v.T, x, axis=1, initial=0)
    psiu = integrate.cumtrapz(u.T, y, axis=0, initial=0)

    return ((-psiu + psiv[0]) + (psiv - psiu[:, 0][:, None])) / 2
