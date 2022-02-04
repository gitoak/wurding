import { Story, Meta } from '@storybook/react';
import { WebUi, WebUiProps } from './WebUi';

export default {
  component: WebUi,
  title: 'WebUi',
} as Meta;

const Template: Story<WebUiProps> = (args) => <WebUi {...args} />;

export const Primary = Template.bind({});
Primary.args = {};
