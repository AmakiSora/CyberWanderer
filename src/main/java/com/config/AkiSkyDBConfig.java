package com.config;

import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.SqlSessionTemplate;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

import javax.sql.DataSource;

@Configuration
@MapperScan(basePackages = "com.dao.akiskyDao",sqlSessionFactoryRef = "akiskydbSqlSessionFactory")
public class AkiSkyDBConfig {
    @Value("${spring.akiskydb.datasource.driver-class-name}")
    String driverClass;
    @Value("${spring.akiskydb.datasource.url}")
    String url;
    @Value("${spring.akiskydb.datasource.username}")
    String userName;
    @Value("${spring.akiskydb.datasource.password}")
    String passWord;
    @Bean(name = "akiskydbDataSource")
    @ConfigurationProperties("spring.akiskydb.datasource")
    public DataSource masterDataSource(){
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        dataSource.setDriverClassName(driverClass);
        dataSource.setUrl(url);
        dataSource.setUsername(userName);
        dataSource.setPassword(passWord);
        return dataSource;
    }
    @Bean(name = "akiskydbSqlSessionFactory")
    public SqlSessionFactory sqlSessionFactory(@Qualifier("akiskydbDataSource") DataSource dataSource) throws Exception {
        SqlSessionFactoryBean sessionFactoryBean = new SqlSessionFactoryBean();
        sessionFactoryBean.setDataSource(dataSource);
        sessionFactoryBean.setMapperLocations(new PathMatchingResourcePatternResolver()
                .getResources("classpath*:mapper/akiskyMapper/*.xml"));
        //**配置多数据源需要设置驼峰规则，否则不生效**
        org.apache.ibatis.session.Configuration configuration=new org.apache.ibatis.session.Configuration();
        configuration.setMapUnderscoreToCamelCase(true);
        sessionFactoryBean.setConfiguration(configuration);
        return sessionFactoryBean.getObject();
    }
    @Bean(name = "akiskydbSqlSessionTemplate")
    public SqlSessionTemplate sqlSessionFactoryTemplate(@Qualifier("akiskydbSqlSessionFactory")SqlSessionFactory sqlSessionFactory ) throws Exception {
        return new SqlSessionTemplate(sqlSessionFactory);
    }
}
