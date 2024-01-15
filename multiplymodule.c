#include <stdio.h>
#include <httpd.h>
#include <http_protocol.h>
#include <http_config.h>
#include <CL/cl.h>

#define MATRIX_SIZE 2

static cl_context context;
static cl_command_queue command_queue;
static cl_program program;
static cl_kernel kernel;

static int init_opencl() {
    cl_platform_id platform;
    cl_device_id device;

    clGetPlatformIDs(1, &platform, NULL);
    clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, NULL);

    context = clCreateContext(NULL, 1, &device, NULL, NULL, NULL);
    command_queue = clCreateCommandQueue(context, device, 0, NULL);

    const char* kernel_source =
        "__kernel void matrix_multiply(__global int* A, __global int* B, __global int* C) {"
        "    int row = get_global_id(0);"
        "    int col = get_global_id(1);"
        "    int sum = 0;"
        "    for (int i = 0; i < MATRIX_SIZE; ++i) {"
        "        sum += A[row * MATRIX_SIZE + i] * B[i * MATRIX_SIZE + col];"
        "    }"
        "    C[row * MATRIX_SIZE + col] = sum;"
        "}";

    program = clCreateProgramWithSource(context, 1, &kernel_source, NULL, NULL);
    clBuildProgram(program, 1, &device, NULL, NULL, NULL);
    kernel = clCreateKernel(program, "matrix_multiply", NULL);

    return 1;
}

static int matrix_multiply_handler(request_rec *r) {
    if (strcmp(r->handler, "matrix_multiply") != 0) {
        return DECLINED;  // Not our handler
    }

    ap_set_content_type(r, "text/plain");

    static int opencl_initialized = 0;
    if (!opencl_initialized) {
        opencl_initialized = init_opencl();
    }

   
    int A[MATRIX_SIZE][MATRIX_SIZE] = {{1, 2}, {3, 4}};
    int B[MATRIX_SIZE][MATRIX_SIZE] = {{5, 6}, {7, 8}};
    int C[MATRIX_SIZE][MATRIX_SIZE];

    // Allocate OpenCL buffers
    cl_mem buffer_A = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(int) * MATRIX_SIZE * MATRIX_SIZE, A, NULL);
    cl_mem buffer_B = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(int) * MATRIX_SIZE * MATRIX_SIZE, B, NULL);
    cl_mem buffer_C = clCreateBuffer(context, CL_MEM_WRITE_ONLY, sizeof(int) * MATRIX_SIZE * MATRIX_SIZE, NULL, NULL);

  
    clSetKernelArg(kernel, 0, sizeof(cl_mem), &buffer_A);
    clSetKernelArg(kernel, 1, sizeof(cl_mem), &buffer_B);
    clSetKernelArg(kernel, 2, sizeof(cl_mem), &buffer_C);

    // Execute the kernel
    size_t global_work_size[2] = {MATRIX_SIZE, MATRIX_SIZE};
    clEnqueueNDRangeKernel(command_queue, kernel, 2, NULL, global_work_size, NULL, 0, NULL, NULL);
    clFinish(command_queue);

  
    clEnqueueReadBuffer(command_queue, buffer_C, CL_TRUE, 0, sizeof(int) * MATRIX_SIZE * MATRIX_SIZE, C, 0, NULL, NULL);

  
    clReleaseMemObject(buffer_A);
    clReleaseMemObject(buffer_B);
    clReleaseMemObject(buffer_C);

    // Print the result
    for (int i = 0; i < MATRIX_SIZE; ++i) {
        for (int j = 0; j < MATRIX_SIZE; ++j) {
            ap_rprintf(r, "%d ", C[i][j]);
        }
        ap_rputs("\n", r);
    }

    return OK;
}

static void register_hooks(apr_pool_t *p) {
    ap_hook_handler(matrix_multiply_handler, NULL, NULL, APR_HOOK_LAST);
}

module AP_MODULE_DECLARE_DATA matrix_multiply_module = {
    STANDARD20_MODULE_STUFF,
    NULL,                 
    NULL,                 
    NULL,                
    NULL,                 
    NULL,                 
    register_hooks        
};


//Add this to the .conf file:
//# httpd.conf

//LoadModule matrix_multiply_module modules/mod_matrix.so

//<Location "/matrix_multiply">
    //SetHandler matrix_multiply
//</Location>