package za.co.wethinkcode.movie;

import java.time.LocalDate;

public class Person {
    private String name;
    private LocalDate birthDate;

    public Person(String name, LocalDate birthDate) {
        if (name == null) {
            throw new NullPointerException("Name may not be null");
        }
        if (name.isEmpty()) {
            throw new IllegalArgumentException("Name may not be empty");
        }

        LocalDate now = LocalDate.now();
        if (birthDate != null && now.isBefore(birthDate)) {
            throw new IllegalArgumentException("Birth date must be in the past or null");
        }

        this.name = name;
        this.birthDate = birthDate;
    }

    public Person(String name) {
        this(name, null);
    }

    public String name() {
        return name;
    }

    public LocalDate birthDate() {
        return birthDate;
    }

    public String asFormattedString() {
        String result = "Name: " + name;
        if (birthDate != null) {
            result += "\nBirth Date: " + birthDate;
        } else {
            result += "\nBirth Date: Unknown";
        }
        return result;
    }
}