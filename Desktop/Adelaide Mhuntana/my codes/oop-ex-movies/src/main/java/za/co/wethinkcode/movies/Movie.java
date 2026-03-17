package za.co.wethinkcode.movies;

import java.time.Duration;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class Movie {
    private final String title;
    private String synopsis;
    private LocalDate releaseDate;
    private final Person director;
    private final Duration runtime;
    private List<Person> actors;

    public Movie(String title, String synopsis, LocalDate releaseDate,
                 Person director, Duration runtime) {
        // Validate title
        if (title == null) {
            throw new NullPointerException("Title may not be null");
        }
        if (title.isEmpty()) {
            throw new IllegalArgumentException("Title may not be empty");
        }

        // Validate release date
        if (releaseDate == null) {
            throw new NullPointerException("Release date may not be null");
        }

        // Validate director
        if (director == null) {
            throw new NullPointerException("Director may not be null");
        }

        // Validate runtime
        if (runtime == null) {
            throw new NullPointerException("Runtime may not be null");
        }

        this.title = title;
        this.synopsis = (synopsis == null) ? "" : synopsis;
        this.releaseDate = releaseDate;
        this.director = director;
        this.runtime = runtime;
        this.actors = new ArrayList<>();
    }

    // Getters
    public String getTitle() {
        return title;
    }

    public String getSynopsis() {
        return synopsis;
    }

    public LocalDate getReleaseDate() {
        return releaseDate;
    }

    public Person getDirector() {
        return director;
    }

    public Duration getRuntime() {
        return runtime;
    }

    // Setters
    public void setSynopsis(String synopsis) {
        this.synopsis = (synopsis == null) ? "" : synopsis;
    }

    public void setReleaseDate(LocalDate newDate) {
        if (newDate == null) {
            throw new NullPointerException("Release date may not be null");
        }

        LocalDate now = LocalDate.now();
        if (newDate.isAfter(now) || newDate.isEqual(now)) {
            this.releaseDate = newDate;
        } else {
            throw new IllegalArgumentException("Release date can only be changed to future dates");
        }
    }

    // Version 2 methods
    public boolean isReleased() {
        LocalDate now = LocalDate.now();
        return releaseDate.isBefore(now);
    }

    public void addActor(Person anActor) {
        if (anActor == null) {
            throw new NullPointerException("Actor may not be null");
        }
        actors.add(anActor);
    }

    public List<Person> allActors() {
        return new ArrayList<>(actors);
    }

    public int numberOfActors() {
        return actors.size();
    }

    public String asFormattedString() {
        return "Title: " + title + "\n" +
                "Synopsis: " + synopsis + "\n" +
                "Release Date: " + releaseDate + "\n" +
                "Director: " + director.name() + "\n" +
                "Runtime: " + runtime.toHours() + " hours " +
                runtime.toMinutesPart() + " minutes";
    }
}