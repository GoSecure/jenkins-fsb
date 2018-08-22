SOURCE="$(dirname "$0")"

java -cp "$SOURCE/lib/*" edu.umd.cs.findbugs.LaunchAppropriateUI -quiet -pluginList $SOURCE/lib/findsecbugs-plugin-1.8.0.jar -include $SOURCE/include.xml $@
