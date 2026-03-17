package za.co.wethinkcode.movies;

import java.time.Duration;
import java.time.LocalDate;

public class MovieApp {

    public static void main(String[] args) {
        System.out.println("=== Movie Exercise ===\n");

        // Create directors using your Person class
        Person director1 = new Person("Christopher Nolan", LocalDate.of(1970, 7, 30));
        Person director2 = new Person("Greta Gerwig");
        Person director3 = new Person("Martin Scorsese", LocalDate.of(1942, 11, 17));

        // Create actors
        Person actor1 = new Person("Leonardo DiCaprio");
        Person actor2 = new Person("Margot Robbie");

        // Create movies
        Movie movie1 = new Movie(
                "Inception",
                "A thief who steals corporate secrets through dream-sharing",
                LocalDate.of(2010, 7, 16),
                director1,
                Duration.ofHours(2).plusMinutes(28)
        );

        movie1.addActor(actor1);
        printMovieDetails(movie1);

        Movie movie2 = new Movie(
                "Barbie",
                "Barbie suffers a crisis that leads her to question her world",
                LocalDate.of(2025, 7, 21),
                director2,
                Duration.ofHours(1).plusMinutes(54)
        );

        movie2.addActor(actor2);
        printMovieDetails(movie2);
    }

    private static void printMovieDetails(Movie movie) {
        System.out.println(movie.asFormattedString());
        System.out.println("Actors (" + movie.numberOfActors() + "):");
        for (Person actor : movie.allActors()) {
            System.out.println("  - " + actor.name());
        }
        System.out.println("Released? " + (movie.isReleased() ? "Yes" : "No"));
        System.out.println("------------------------\n");
    }
}