#include<stdio.h>
#include<string.h>

int printf(const char *format, ...);
int scanf(const char *format, ...);
int memset(char *str, int c, int n);


//void swap(int* a, int* b) {
//    int t = *a;
//    *a = *b;
//    *b = t;
//}

int partition (int *arr, int low, int high)
{
    int pivot = arr[high];    // pivot
    int i = low - 1;  // Index of smaller element

    for (int j = low; j <= high- 1; j++)
    {
        // If current element is smaller than the pivot
        if (arr[j] < pivot)
        {
            i++;    // increment index of smaller element
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }

    int temp = arr[i+1];
    arr[i+1] = arr[high];
    arr[high] = temp;
//    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

void quickSort(int *arr, int low, int high)
{
    if (low < high)
    {
        /* pi is partitioning index, arr[p] is now
           at right place */
        int pi = partition(arr, low, high);

        // Separately sort elements before
        // partition and after partition
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

void printArray(int *arr, int size)
{
    int i;
    for (i=0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

// Driver program to test above functions
int main()
{
    int n;
    int arr[256];
    for (int i = 0; i < 256; i++) {
        arr[i] = 0;
    }
    printf("size of array to sort:");
    scanf("%d", &n);
    printf("origin array:\n");
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }
    quickSort(arr, 0, n-1);
    printf("sorted array: \n");
    printArray(arr, n);
    return 0;
}