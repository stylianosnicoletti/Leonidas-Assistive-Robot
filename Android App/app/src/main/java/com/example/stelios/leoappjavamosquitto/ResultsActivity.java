package com.example.stelios.leoappjavamosquitto;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.Html;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;


public class ResultsActivity extends AppCompatActivity {
    private ListView listView;
    private ArrayAdapter<String> listAdapter ;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.results);
        String data = (String)getIntent().getSerializableExtra("data");

        if (data.substring(0, 1).equals("R")) {
            final TextView display = findViewById(R.id.textView2);
            display.setText(data);
        }

        if(data.substring(0, 1).equals("S")) {
            final TextView display = findViewById(R.id.textView2);
            display.setText("Congratulations! Your accuracy is ");
            final TextView score = findViewById(R.id.textView);
            score.setText(data);
        }

        if(data.length() <=6) {
            final TextView display = findViewById(R.id.textView2);
            display.setText("Your response time was");
            final TextView score = findViewById(R.id.textView);
            score.setText(data + " " + "seconds");
        }
    }
}
