package org.example.Demo;

import java.util.ArrayDeque;
import java.util.Queue;

public class demo2 {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        Queue<Integer> queue = new ArrayDeque<>();
        for (int j = 0; j < n; j++) {
            for (int i = n - 1; i >= 0; i--) {
                queue.offer(matrix[i][j]);
            }
        }
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++)
                matrix[i][j] = queue.poll();
        }
    }
}
