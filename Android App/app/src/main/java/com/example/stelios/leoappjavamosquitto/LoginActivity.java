package com.example.stelios.leoappjavamosquitto;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.parse.LogInCallback;
import com.parse.Parse;
import com.parse.ParseException;
import com.parse.ParseUser;
import com.parse.SignUpCallback;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Parse.initialize(new Parse.Configuration.Builder(this)
                .applicationId("tIdJ4EevU1yCdQQJ6fJhqxKlFiRgUjP1DUEzfeWc")
                .clientKey("iqnNgPLywTB0mV1Hjtuf9aLkCZxDvLFYE57AFEut")
                .server("https://parseapi.back4app.com/").build());

        final EditText mEmail = findViewById((R.id.editText3));
        final EditText mPassword = findViewById(R.id.editText4);
        Button mRegister = findViewById(R.id.button5);
        Button mLogin = findViewById(R.id.button6);
        ParseUser.getCurrentUser().logOut();


        mLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                final String email = mEmail.getText().toString();
                String username = email.substring(0, email.indexOf("@"));
                String password = mPassword.getText().toString();

                ParseUser.logInInBackground(username, password, new LogInCallback() {
                    @Override
                    public void done(ParseUser parseUser, ParseException e) {
                        if (parseUser != null) {
                            /*Context context = getApplicationContext();
                            CharSequence text = "Login successful!";
                            int duration = Toast.LENGTH_SHORT;
                            Toast.makeText(context, text, duration).show();*/
                            Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                            intent.putExtra("email", email);
                            startActivity(intent);
                        } else {
                            Context context = getApplicationContext();
                            CharSequence text = "Login not successful!";
                            int duration = Toast.LENGTH_SHORT;
                            Toast.makeText(context, text, duration).show();
                        }
                    }
                });
            }
        });

        mRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String email = mEmail.getText().toString();
                String username = email.substring(0, email.indexOf("@"));
                String password = mPassword.getText().toString();

                Log.d("email", email);
                Log.d("username", username);
                Log.d("password", password);

                ParseUser user = new ParseUser();
                user.setUsername(username);
                user.setEmail(email);
                user.setPassword(password);
                user.signUpInBackground(new SignUpCallback() {
                    @Override
                    public void done(ParseException e) {
                        if (e == null) {
                            Context context = getApplicationContext();
                            CharSequence text = "Registration successful! You can now login";
                            int duration = Toast.LENGTH_SHORT;
                            Toast.makeText(context, text, duration).show();
                        } else {
                            Context context = getApplicationContext();
                            CharSequence text = "Register failed!";
                            int duration = Toast.LENGTH_SHORT;
                            Toast.makeText(context, text, duration).show();
                        }
                    }
                });
            }
        });
    }

}
