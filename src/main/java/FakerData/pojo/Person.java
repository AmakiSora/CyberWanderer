package FakerData.pojo;

import lombok.Data;

import java.util.Date;

@Data
public class Person {
    private int id;
    private String last_name;
    private String first_name;
    private String city;
    private Date birth_date;
    private String gender;
    private String phone;
    private String email;
}
