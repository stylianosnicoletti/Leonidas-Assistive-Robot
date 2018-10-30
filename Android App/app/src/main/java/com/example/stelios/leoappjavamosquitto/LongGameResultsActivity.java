package com.example.stelios.leoappjavamosquitto;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

public class LongGameResultsActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_long_game_results);

        //GraphView graph = (GraphView) findViewById(R.id.graph);
        String data = (String)getIntent().getSerializableExtra("data");
        String [] tokens = data.split(",\\s");

        final TextView display = findViewById(R.id.textView6);
        display.setText(tokens[0] + " " + "seconds");

        final TextView display2 = findViewById(R.id.textView7);
        display2.setText(tokens[1] + " " + "seconds");

        final TextView display3 = findViewById(R.id.textView8);
        display3.setText(tokens[2] + " " + "seconds");

        final TextView display4 = findViewById(R.id.textView9);
        display4.setText(tokens[3] + " " + "seconds");

        final TextView display5 = findViewById(R.id.textView4);
        display5.setText(tokens[4] + " " + "seconds");
    }
}
