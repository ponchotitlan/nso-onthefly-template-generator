# On-The-Fly Template Generator Action Package

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/ponchotitlan/nso-onthefly-template-generator)

This action package creates a new device template in NSO CDB by parsing input CLI native configurations into template-friendly XML outputs.

The action package creates a temporary dummy device which is used for parsing the input configuration into compliant XML payload, which is later pushed into CDB as a device template ready for use. The temporary dummy device is deleted afterwards.

```
         Action package
        +--------------------------------------------------------------------+                                 
        |                                                                    |                                 
        |                   +-----------------+                              |                                 
        |                   |                 |                              |                                 
        |                   |                 | Device template              |                                 
        |  Raw CLI config   |  Temporary      | compliant      +----------+  |                                 
        |  (multi-line)     |  dummy device   | XML payload    |          |  |                                 
        |  ---------------->-  created with   |--------------->| NSO CDB  |  |                                 
        |                   |  the specified  |                |          |  |                                 
        |                   |  NED            |                +----------+  |                                 
        |                   |                 |                              |                                 
        |                   |                 |                              |                                 
        |                   +-----------------+                              |                                 
        |                                                                    |                                 
        +--------------------------------------------------------------------+ 
```

## Prerequisites
- The NCS minimum version is v5.5
- Python minimum version is v.2.7.5
- Local and System NCS installs are compliant

## Getting started
Clone the github repository or download the build:
```
git clone https://github.com/ponchotitlan/nso-onthefly-template-generator.git
```
Copy the package content in the location of your NCS environment depending on the type of deployment:

- System Install:
```
/var/opt/ncs/packages/
```

- Local Install:
```
/your_install/packages/
```

The package is not precompiled, therefore it is neccessary to issue the compilation in the src folder:
```
# make /packages/onthefly_template_generator/src/
```

## Usage
The action package supports the following usage:
```
user@ncs# onthefly-template-generator generate ?
Possible completions:
  native-configuration   CLI raw native configuration for template creation.
  ned-id                 Device ned-id to create device template.
  template-name          New template name.
```

The following example demonstrates a successful run
```
user@ncs# onthefly-template-generator generate ned-id cisco-ios-cli-6.69 template-name ComplianceMonday native-configuration  
Value for 'native-configuration' (<string>): 
[Multiline mode, exit with ctrl-D.]
> interface GigabitEthernet1/2
> description Monday
> 
> interface GigabitEthernet1/3
> description Tuesday
> 
result SUCCESS
info Device template (ComplianceMonday) created!
<config xmlns="http://tail-f.com/ns/config/1.0">
  <devices xmlns="http://tail-f.com/ns/ncs">
    <template>
          <name>ComplianceMonday</name>
          <ned-id>
            <id xmlns:cisco-ios-cli-6.69="http://tail-f.com/ns/ned-id/cisco-ios-cli-6.69">cisco-ios-cli-6.69:cisco-ios-cli-6.69</id>
            <config>
              
      <interface xmlns="urn:ios">
        <GigabitEthernet>
          <name>1/2</name>
          <description>Monday</description>
        </GigabitEthernet>
        <GigabitEthernet>
          <name>1/3</name>
          <description>Tuesday</description>
        </GigabitEthernet>
      </interface>
    
            </config>
          </ned-id>
        </template>
  </devices>
</config>
user@ncs#
System message at 2022-02-01 12:17:20...
Commit performed by admin via tcp using generate.
```

The specified template now exists in CDB and is ready for use
```
user@ncs(config)# show full-configuration devices template ComplianceMonday 
devices template ComplianceMonday
 ned-id cisco-ios-cli-6.69
  config
   interface GigabitEthernet 1/2
    description Monday
   !
   interface GigabitEthernet 1/3
    description Tuesday
   !
  !
 !
!
```

Additionally, the tasks performed by this action package are logged in the default logging location
```
<INFO> 01-Feb-2022::12:17:18.511 onthefly-template-generator ncs-dp-20920-onthefly-template-generator:main-2-usid-546-onthefly-template-generator-action: - action name: generate
<INFO> 01-Feb-2022::12:17:18.903 onthefly-template-generator ncs-dp-20920-onthefly-template-generator:main-2-usid-546-onthefly-template-generator-action: - Dummy Device (bfb4e_device) created!
<INFO> 01-Feb-2022::12:17:20.465 onthefly-template-generator ncs-dp-20920-onthefly-template-generator:main-2-usid-546-onthefly-template-generator-action: - 
      <interface xmlns="urn:ios">
        <GigabitEthernet>
          <name>1/2</name>
          <description>Monday</description>
        </GigabitEthernet>
        <GigabitEthernet>
          <name>1/3</name>
          <description>Tuesday</description>
        </GigabitEthernet>
      </interface>
    
<INFO> 01-Feb-2022::12:17:20.749 onthefly-template-generator ncs-dp-20920-onthefly-template-generator:main-2-usid-546-onthefly-template-generator-action: - Device template (ComplianceMonday) created!
<config xmlns="http://tail-f.com/ns/config/1.0">
  <devices xmlns="http://tail-f.com/ns/ncs">
    <template>
          <name>ComplianceMonday</name>
          <ned-id>
            <id xmlns:cisco-ios-cli-6.69="http://tail-f.com/ns/ned-id/cisco-ios-cli-6.69">cisco-ios-cli-6.69:cisco-ios-cli-6.69</id>
            <config>
              
      <interface xmlns="urn:ios">
        <GigabitEthernet>
          <name>1/2</name>
          <description>Monday</description>
        </GigabitEthernet>
        <GigabitEthernet>
          <name>1/3</name>
          <description>Tuesday</description>
        </GigabitEthernet>
      </interface>
    
            </config>
          </ned-id>
        </template>
  </devices>
</config>
<INFO> 01-Feb-2022::12:17:20.991 onthefly-template-generator ncs-dp-20920-onthefly-template-generator:main-2-usid-546-onthefly-template-generator-action: - Dummy device deleted: bfb4e_device
```
