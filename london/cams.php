class JamCamArchive
{
const INPUTXML = "https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk";
const ARCHVEFOLDER = "styles/images/jamcams";

public function runTest()
{
    if (!is_dir(self::ARCHVEFOLDER)) {
        mkdir(self::ARCHVEFOLDER);
    }
    $objDOMdoc = new DOMDocument();
    $objDOMdoc->loadXML(file_get_contents(self::INPUTXML));
    $xpath = new DOMXPath($objDOMdoc);
    $strQuery = "//*";
    {
        $entries = $xpath->query($strQuery);
        foreach ($entries as $entry)
            if ($entry->nodeName == "Contents") {
                if ($entry->hasChildNodes()) {
                    foreach ($entry->childNodes as $node) {
                        if ($node->nodeName == "Key") {
                            $strKey = ($node->nodeValue);
                        }
                        if ($node->nodeName == "LastModified") {
                            $LastModified = ($node->nodeValue);
                        }
                    }
                }
                $strArchiveFilename = self::ARCHVEFOLDER . "/{$strKey}/{$LastModified}." . pathinfo($strKey, PATHINFO_EXTENSION);
                $strArchiveFilename = strtr($strArchiveFilename, [":" => "_"]);
                if (!is_dir(self::ARCHVEFOLDER . "/$strKey")) {
                    mkdir(self::ARCHVEFOLDER . "/$strKey");
                }
                if (!file_exists($strArchiveFilename)) {
                    $strSrc = self::INPUTXML . "/$strKey";
                    file_put_contents($strArchiveFilename, file_get_contents($strSrc));
                    echo PHP_EOL . "copy $strArchiveFilename";
                } else {
                    echo "*";
                }
            }
    }
}
}
