var PythonShell = require('python-shell')

var myArgs = process.argv.slice(2)

var option_args = ['--url',myArgs[0], '--pwd', myArgs[1]];

if (myArgs[2] == 'copy_files'){
  option_args.push('--copy_files');
}

var options = {
    args: option_args
  };

PythonShell.run('regenerate_api_data.py', options,function (err) {
    if (err) throw err;
    console.log('completed');
  });
