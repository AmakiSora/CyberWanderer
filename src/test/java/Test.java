import org.jasypt.encryption.StringEncryptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
public class Test {
    @Autowired
    StringEncryptor encryptor;
    @org.junit.jupiter.api.Test
    void T(){
        String name = encryptor.encrypt("");
        String password = encryptor.encrypt("");
        System.out.println(name+"----------------");
        System.out.println(password+"----------------");
    }
}
