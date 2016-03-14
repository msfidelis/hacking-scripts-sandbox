<?php

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 * Description of uploadIBGEController
 *
 * @author matheus
 */
class uploadibge {

    private $fieldseparator = ";";
    private $lineseparator = "\n";
    private $sqlfile = "/var/www/html/gestorsuporte/gestorfox/cache/etc/ibegedados.sql";
    private $file = "/var/www/html/gestorsuporte/gestorfox/cache/etc/ibge.csv";

    public function index_action() {

        $class = new SplFileObject($this->file);
        $class->setFlags(SplFileObject::SKIP_EMPTY | SplFileObject::DROP_NEW_LINE);
        $class->setCsvControl($this->fieldseparator);

        $data = array();
        ob_start();

        for ($i = 0; !$class->eof(); $i++) {
            $data_array = $class->fgetcsv();
            $estado = $this->dadosEstado($data_array);

            $municipio = $this->letrasMaiusculaSemAcento($data_array[3]);
            $sql = "UPDATE erp_municipio SET cod_ibge = $data_array[4] WHERE des = UPPER('{$municipio}') AND id_estado = $estado; \n";

            $this->writeData($sql);

            var_dump($sql);
            ob_flush();
            flush();
        }
    }

    public function dadosEstado($data_array) {
        $model = new municipioModel();

        $estado = util::letrasMaiusculaSemAcento($data_array[1]);
        $where = "e.des = UPPER('{$estado}') GROUP BY id_estado";

        return $model->getMunicipio($where)[0]['id_estado'];
    }

    public function writeData($sql) {
        $file = fopen($this->sqlfile, "a");
        fwrite($file, $sql);
        fclose($file);
        return true;
    }

    public function letrasMaiusculaSemAcento($string) {
        setlocale(LC_ALL, 'en_US.UTF8');
        $trata_string = preg_replace('/[`^~\'"\\\]/', null, iconv('UTF-8', 'ASCII//TRANSLIT', $string));
        return strtoupper($trata_string);
    }

}

