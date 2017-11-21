/* The next line is to tell emacs' javascript mode that c3 is defined
 * externally, otherwise it sees it as an error. */
/* global c3 d3 */

function load_chart_callback(err, data)
{
    if (err) {
        alert(err);
    }
    /* we have the json in the weird format generated by multi-perf-test,
       and we need to convert it to the weird format used by c3.

       loaded data looks like:

       [
         [ "commit id 1",
           {
             "test name 1" : <number>,
             "test name 2" : <number>, ...
           }
         ],
         [ "commit id 2",
           {
             "test name 1" : <number>,
             "test name 2" : <number>, ...
           }
         ], ...

       where the same commit id is  expected to occur multiple times.
       Usually we pick the lowest.

     c3 wants:

     [
       ['test name 1', <number>,  <number>, ...],
       ['test name 2', <number>,  <number>, ...],...
     ]

     and
       ['x', 'commit id 1',  'commit id 2',...]


       let's do it in steps.
    */
    var i, j, d, c, t;

    var commits = [];
    for (i = 0; i < data.length; i++) {
        c = data[i][0];
        if (c === commits[0]) {
            break;
        }
        commits.push(c);
    }
    console.log(data);
    var tests = [];
    for (t in data[0][1]) {
        tests.push(t);
    }
    tests.sort();

    var tmp = {};
    for (i = 0; i < data.length; i++) {
        c = data[i][0];
        var results = data[i][1];
        for (t in results) {
            if (tmp[t] === undefined) {
                tmp[t] = {};
            }
            d = tmp[t];
            if (d[c] === undefined) {
                d[c] = [];
            }
            if (results[t]) {
                d[c].push(results[t]);
            }
        }
    }
    /* squash down to the minimum */
    for (t in tmp) {
        d = tmp[t];
        for (c in d) {
            d[c] = Math.min.apply(null, d[c]);
        }
    }

    var reformatted = [];

    for (j = 0; j < tests.length; j++) {
        t = tests[j];
        var tidy = t.match(/.+__main__\..+\.test_(?:\d+_\d+_)?(.+?)(?:\(ad_dc_ntvfs\))?$/);
        var line = [tidy[1] || t];
        for (i = 0; i < commits.length; i++) {
            c = commits[i];
            line.push(tmp[t][c] || null);
        }
        reformatted.push(line);
    }

    //console.log(reformatted);
    var chart = c3.generate({
        bindto: '#chart',
        data: {
            columns: reformatted
      },
      size: {
          height: 1800,
          width: 800
      },
      zoom: {
          enabled: true,
          rescale: true
      }
    });
    return chart;
}


function load_chart(url)
{
    d3.json(url, load_chart_callback);
}