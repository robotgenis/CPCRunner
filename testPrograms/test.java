package testPrograms;

import java.util.Scanner;

public class test {
	public static void main(String[] args) {
		Scanner readme = new Scanner(System.in);
		// two variables to hold numbers

		int n = readme.nextInt();
		for (int i = 0; i < n; i++)
			System.out.println(readme.nextInt() + readme.nextInt());

	}
}